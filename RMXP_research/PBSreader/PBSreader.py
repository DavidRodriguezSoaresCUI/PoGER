import pbEngine
from pathlib import Path


def main():
    cwd = Path()
    print(f'PROGRAM BEGIN, cwd={cwd.resolve()}')
    PBSlocation = cwd.joinpath('PBS')
    assert PBSlocation.is_dir(), f'{PBSlocation} directory not found !'

    import time 
    start = time.time()
    engine = pbEngine.pbEngine( PBSlocation, demo=False )
    print(f'Loaded PBS in {round((time.time()-start)*1000)} ms.')
    print('END OF PROGRAM')


if __name__ == '__main__':
    main()