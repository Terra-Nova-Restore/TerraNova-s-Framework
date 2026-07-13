import argparse,hashlib,json,logging,os,re,sys,time
from datetime import datetime,timezone
from pathlib import Path
import requests
from preflight import preflight_check, PreflightError

VALID_MODES={'full','dry-run','validate'}
OFFLINE_MODE='offline-validate'
OFFLINE_WORKFLOW='.github/workflows/tnv_notion_to_github.yml'
OFFLINE_EXPECTED_MAPPING={
    'export_flag_property':'Export_to_GitHub',
    'url_property':'GitHub_Issue_URL',
    'date_property':'Exported_At',
    'title_field':'Change_ID',
}

class OfflineValidationError(RuntimeError):
    """Public-safe repository-only validation failure."""

def setup_logging(d):
    Path(d).mkdir(parents=True,exist_ok=True)
    ts=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    logging.basicConfig(level=logging.INFO,format='%(asctime)s %(message)s',
        handlers=[logging.FileHandler(Path(d)/f'tnv_{ts}.log'),logging.StreamHandler(sys.stdout)])
    return logging.getLogger('tnv')

class NC:
    B='https://api.notion.com/v1'
    def __init__(self,t):
        self.s=requests.Session()
        self.s.headers.update({'Authorization':f'Bearer {t}','Notion-Version':'2022-06-28','Content-Type':'application/json'})
    def query(self,db,f=None):
        pp,c=[],None
        while True:
            b={'page_size':100}
            if f:b['filter']=f
            if c:b['start_cursor']=c
            r=self.s.post(f'{self.B}/databases/{db}/query',json=b);r.raise_for_status();d=r.json()
            pp+=d.get('results',[])
            if not d.get('has_more'):break
            c=d.get('next_cursor')
        return pp
    def update(self,pid,props):
        self.s.patch(f'{self.B}/pages/{pid}',json={'properties':props}).raise_for_status()

class GH:
    B='https://api.github.com'
    def __init__(self,t,repo):
        self.repo=repo;self.s=requests.Session()
        self.s.headers.update({'Authorization':f'Bearer {t}','Accept':'application/vnd.github+json'})
    def issue(self,title,body,labels=None):
        p={'title':title,'body':body}
        if labels:p['labels']=labels
        r=self.s.post(f'{self.B}/repos/{self.repo}/issues',json=p);r.raise_for_status();return r.json()
    def find_issue_by_title_exact(self,title):
        page=1
        while True:
            r=self.s.get(f'{self.B}/repos/{self.repo}/issues',params={'state':'all','per_page':100,'page':page})
            r.raise_for_status()
            issues=r.json()
            if not issues:return None
            for issue in issues:
                if issue.get('pull_request'):continue
                if issue.get('title')==title:return issue
            if len(issues)<100:return None
            page+=1

def gtxt(p):
    t=p.get('type','')
    return ''.join(x.get('plain_text','') for x in(p.get('title',[]) if t=='title' else p.get('rich_text',[]))).strip()

def body(props,cfg):
    lines=['## TerraNova Change\n']
    for f in cfg.get('body_fields',[]):
        k=f.get('notion_key','');lbl=f.get('label',k)
        if k not in props:continue
        p=props[k];t=p.get('type','')
        v=gtxt(p) if t in('title','rich_text') else str(p.get('checkbox','')) if t=='checkbox' else (p.get('select') or {}).get('name','') if t=='select' else p.get('url','') if t=='url' else ''
        if v:lines.append(f'**{lbl}:** {v}')
    lines.append(f'\n---\n*TNV-Auto {datetime.now(timezone.utc).isoformat()}*')
    return '\n'.join(lines)

def write_shadow_record(shadow_dir,pid,title,url,status):
    Path(shadow_dir).mkdir(parents=True,exist_ok=True)
    (Path(shadow_dir)/f"{pid[:8]}.json").write_text(json.dumps({'pid':pid,'title':title,'url':url,'status':status}))

def _offline_repo_file(root,value,label):
    candidate=Path(value)
    if not candidate.is_absolute():candidate=root/candidate
    try:candidate=candidate.resolve()
    except (OSError,RuntimeError) as exc:raise OfflineValidationError(f'{label.upper()}_PATH_INVALID') from exc
    try:candidate.relative_to(root)
    except ValueError as exc:raise OfflineValidationError(f'{label.upper()}_OUTSIDE_REPOSITORY') from exc
    if not candidate.is_file():raise OfflineValidationError(f'{label.upper()}_FILE_MISSING')
    return candidate

def _offline_validate_config(path):
    try:cfg=json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:raise OfflineValidationError('CONFIG_INVALID_JSON') from exc
    except UnicodeError as exc:raise OfflineValidationError('CONFIG_INVALID_ENCODING') from exc
    except OSError as exc:raise OfflineValidationError('CONFIG_NOT_READABLE') from exc
    if not isinstance(cfg,dict):raise OfflineValidationError('CONFIG_ROOT_NOT_OBJECT')
    invalid=[key for key,value in OFFLINE_EXPECTED_MAPPING.items() if cfg.get(key)!=value]
    if not isinstance(cfg.get('github_repo'),str) or '/' not in cfg['github_repo']:
        invalid.append('github_repo')
    labels=cfg.get('default_labels')
    if not isinstance(labels,list) or not labels or not all(isinstance(item,str) and item for item in labels):
        invalid.append('default_labels')
    body_fields=cfg.get('body_fields')
    if not isinstance(body_fields,list) or not body_fields or not all(
        isinstance(item,dict)
        and isinstance(item.get('notion_key'),str)
        and bool(item.get('notion_key'))
        and isinstance(item.get('label'),str)
        and bool(item.get('label'))
        for item in body_fields
    ):
        invalid.append('body_fields')
    if invalid:raise OfflineValidationError('CONFIG_MAPPING_INVALID:'+','.join(sorted(set(invalid))))
    return {
        'status':'pass',
        'mapping_keys':sorted(OFFLINE_EXPECTED_MAPPING),
        'default_label_count':len(labels),
        'body_field_count':len(body_fields),
    }

def _offline_yaml_records(text):
    records=[]
    for line in text.splitlines():
        leading=line[:len(line)-len(line.lstrip())]
        if '\t' in leading:raise OfflineValidationError('WORKFLOW_INDENTATION_INVALID')
        value=line.strip()
        if not value or value.startswith('#'):continue
        records.append((len(leading),value))
    return records

def _offline_yaml_block(records,key,indent,start=0,end=None):
    limit=len(records) if end is None else end
    for index in range(start,limit):
        current_indent,value=records[index]
        if current_indent==indent and value==f'{key}:':
            block_end=index+1
            while block_end<limit and records[block_end][0]>indent:block_end+=1
            return index+1,block_end
    return None

def _offline_sync_run_present(records,steps_block):
    if not steps_block:return False
    start,end=steps_block
    for index in range(start,end):
        indent,value=records[index]
        if indent!=8 or value not in {'run: |','run: |-','run: |+'}:continue
        step_header=False
        for previous in range(index-1,start-1,-1):
            previous_indent,previous_value=records[previous]
            if previous_indent<6:break
            if previous_indent==6:
                step_header=previous_value.startswith('- ')
                break
        if not step_header:continue
        content_end=index+1
        while content_end<end and records[content_end][0]>indent:content_end+=1
        content=' '.join(value for _,value in records[index+1:content_end])
        if 'python scripts/notion_to_github.py' in content and '--config config/notion_map.json' in content:
            return True
    return False

def _offline_validate_workflow(path):
    try:text=path.read_text(encoding='utf-8')
    except UnicodeError as exc:raise OfflineValidationError('WORKFLOW_INVALID_ENCODING') from exc
    except OSError as exc:raise OfflineValidationError('WORKFLOW_NOT_READABLE') from exc
    records=_offline_yaml_records(text)
    on_block=_offline_yaml_block(records,'on',0)
    schedule_block=_offline_yaml_block(records,'schedule',2,*(on_block or (0,0)))
    permissions_block=_offline_yaml_block(records,'permissions',0)
    jobs_block=_offline_yaml_block(records,'jobs',0)
    sync_block=_offline_yaml_block(records,'sync',2,*(jobs_block or (0,0)))
    steps_block=_offline_yaml_block(records,'steps',4,*(sync_block or (0,0)))
    cron_value=''
    if schedule_block:
        for indent,value in records[schedule_block[0]:schedule_block[1]]:
            cron=re.fullmatch(r'-\s+cron:\s*(["\'])([^"\']+)\1',value)
            if indent==4 and cron:
                cron_value=cron.group(2)
                break
    checks={
        'schedule':cron_value=='*/10 * * * *',
        'workflow_dispatch':bool(on_block and any(
            indent==2 and value=='workflow_dispatch:'
            for indent,value in records[on_block[0]:on_block[1]]
        )),
        'contents_write':bool(permissions_block and any(
            indent==2 and value=='contents: write'
            for indent,value in records[permissions_block[0]:permissions_block[1]]
        )),
        'issues_write':bool(permissions_block and any(
            indent==2 and value=='issues: write'
            for indent,value in records[permissions_block[0]:permissions_block[1]]
        )),
        'sync_run_step':_offline_sync_run_present(records,steps_block),
    }
    failed=sorted(name for name,passed in checks.items() if not passed)
    if failed:raise OfflineValidationError('WORKFLOW_STRUCTURE_INVALID:'+','.join(failed))
    return {
        'status':'pass',
        'schedule_cron':cron_value,
        'workflow_dispatch':True,
        'permissions':['contents:write','issues:write'],
    }

def offline_validate(args):
    root=Path(__file__).resolve().parents[1]
    try:
        config_path=_offline_repo_file(root,args.config,'config')
        workflow_path=_offline_repo_file(root,getattr(args,'workflow',OFFLINE_WORKFLOW),'workflow')
        config_result=_offline_validate_config(config_path)
        workflow_result=_offline_validate_workflow(workflow_path)
        payload={
            'mode':OFFLINE_MODE,
            'status':'pass',
            'config_validation':config_result,
            'workflow_validation':workflow_result,
            'credential_values_read':False,
            'network_calls_performed':False,
            'runtime_artifacts_created':False,
        }
        exit_code=0
    except OfflineValidationError as exc:
        payload={
            'mode':OFFLINE_MODE,
            'status':'blocked',
            'error':str(exc),
            'credential_values_read':False,
            'network_calls_performed':False,
            'runtime_artifacts_created':False,
        }
        exit_code=1
    print(json.dumps(payload,indent=2,ensure_ascii=False,sort_keys=True))
    return exit_code

def main(args):
    if args.mode=='offline-validate':
        return offline_validate(args)
    log=setup_logging(args.log)
    log.info('TNV Sync 521 OK')
    if args.mode not in VALID_MODES:
        log.error(f'Unsupported mode: {args.mode}')
        sys.exit(2)
    cfg=json.loads(Path(args.config).read_text())

    # Run preflight validation
    concurrency=None
    try:
        nd=os.environ.get('NOTION_DATABASE_ID_CHANGES','')
        if not nd:
            log.error('NOTION_DATABASE_ID_CHANGES missing')
            sys.exit(1)
        log.info('Preflight validation starting...')
        results, concurrency = preflight_check(nd, args.config, args.lock_file)
        log.info(f'Preflight passed: {results["passed"]} checks OK')

        # Get secrets (workflow sends NOTION_TOKEN, GH_PAT; also accept NOTION_API_KEY for flexibility)
        nt = os.environ.get('NOTION_TOKEN') or os.environ.get('NOTION_API_KEY','')
        gt = os.environ.get('GH_PAT') or os.environ.get('GITHUB_TOKEN','')
        gr = (
            os.environ.get('TARGET_GITHUB_REPO')
            or os.environ.get('GITHUB_REPO')
            or cfg.get('github_repo','')
        )

        nc=NC(nt);gh=GH(gt,gr)
        ef=cfg.get('export_flag_property','Export_to_GitHub');up=cfg.get('url_property','GitHub_Issue_URL')
        dp=cfg.get('date_property','Exported_At');tf=cfg.get('title_field','Change_ID')
        lb=cfg.get('default_labels',['tnv-auto'])
        pages=nc.query(nd,{'and':[{'property':ef,'checkbox':{'equals':True}},{'property':up,'url':{'is_empty':True}}]})
        log.info(f'{len(pages)} pages pending export in mode={args.mode}')
        processed=[];deduped=[];planned=[]
        if args.mode=='validate':
            Path(args.hash_out).write_text(hashlib.sha256(json.dumps({'mode':args.mode,'pending':len(pages)}).encode()).hexdigest()[:16])
            log.info('Validate mode complete: preflight passed, pending pages counted, no GitHub/Notion writes performed')
            return
        for pg in pages:
            pid=pg['id'];props=pg.get('properties',{})
            title=gtxt(props.get(tf,{})) or f'TNV {pid[:8]}'
            existing=gh.find_issue_by_title_exact(title)
            if existing:
                url=existing['html_url'];log.info(f'Existing issue reused: {url}')
                if args.mode=='full':
                    write_shadow_record(args.shadow,pid,title,url,'deduped')
                    try:nc.update(pid,{up:{'url':url},dp:{'date':{'start':datetime.now(timezone.utc).strftime('%Y-%m-%d')}}})
                    except Exception as e:log.error(e)
                    processed.append(pid)
                deduped.append({'pid':pid,'title':title,'url':url})
                time.sleep(0.1)
                continue
            if args.mode=='dry-run':
                planned.append({'pid':pid,'title':title,'action':'create'})
                log.info(f'Dry-run would create issue: {title}')
                continue
            try:iss=gh.issue(title,body(props,cfg),lb)
            except Exception as e:log.error(e);continue
            url=iss['html_url'];log.info(f'Issue created: {url}')
            write_shadow_record(args.shadow,pid,title,url,'created')
            try:nc.update(pid,{up:{'url':url},dp:{'date':{'start':datetime.now(timezone.utc).strftime('%Y-%m-%d')}}})
            except Exception as e:log.error(e)
            processed.append(pid);time.sleep(0.3)
        h=hashlib.sha256(json.dumps({'mode':args.mode,'processed':processed,'deduped':deduped,'planned':planned}).encode()).hexdigest()[:16]
        Path(args.hash_out).write_text(h)
        log.info(f'Done processed={len(processed)} deduped={len(deduped)} planned={len(planned)} hash:{h}')
    except PreflightError as e:
        log.error(f'Preflight validation failed:\n{str(e)}')
        sys.exit(1)
    finally:
        if concurrency:
            concurrency.release()
            log.info('Sync lock released')

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--mode',default='full',choices=sorted(VALID_MODES|{OFFLINE_MODE}))
    p.add_argument('--shadow',default='shadow/')
    p.add_argument('--log',default='logs/')
    p.add_argument('--hash-out',default='.tnv_hash')
    p.add_argument('--config',default='config/notion_map.json')
    p.add_argument('--workflow',default=OFFLINE_WORKFLOW)
    p.add_argument('--lock-file',default='.tnv_sync.lock')
    exit_code=main(p.parse_args())
    if isinstance(exit_code,int):raise SystemExit(exit_code)
