import argparse,hashlib,json,logging,os,sys,time
from datetime import datetime,timezone
from pathlib import Path
import requests
from preflight import preflight_check, PreflightError

VALID_MODES={'full','dry-run','validate'}

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

def main(args):
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
    p.add_argument('--mode',default='full',choices=sorted(VALID_MODES))
    p.add_argument('--shadow',default='shadow/')
    p.add_argument('--log',default='logs/')
    p.add_argument('--hash-out',default='.tnv_hash')
    p.add_argument('--config',default='config/notion_map.json')
    p.add_argument('--lock-file',default='.tnv_sync.lock')
    main(p.parse_args())
