# 概要
KEGGパスウェイに対してのproteomeしたい時に使えるスクリプト

## スクリプト詳細
使う順に記述する

- get_pathway_info.py: パスウェイに対して情報を取得するスクリプト(pathway_info.csv)
- get_pdbid.py: pathway_infoからPDB IDを抜き出すスクリプト(pdb_list.csv)
- get_pdb_file.py: wgetで指定されたファイルにかかれているPDBファイルを取得する
- filter_and_split.py: python filter_and_split.py (target dir) (outputdir) で解像度，残基数でフィルタ 