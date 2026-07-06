from pathlib import Path
import argparse, json, os
import cfbd

RAW_ROOT=Path('data/raw/games')

def build_client():
    cfg=cfbd.Configuration(access_token=os.environ['CFBD_API_KEY'])
    return cfbd.GamesApi(cfbd.ApiClient(cfg))

def acquire_season(season:int):
    api=build_client()
    games=api.get_games(year=season, classification='fbs')
    out=RAW_ROOT/str(season)
    out.mkdir(parents=True, exist_ok=True)
    with (out/'games.json').open('w',encoding='utf-8') as f:
        json.dump([g.to_dict() if hasattr(g,'to_dict') else g for g in games],f,indent=2,default=str)

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--season',type=int,required=True)
    args=ap.parse_args()
    acquire_season(args.season)
