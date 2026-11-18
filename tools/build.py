# src/ と art/ から、遊べる 1 ファイルの index.html を組み立てる
import json, os, base64
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
p = lambda *a: os.path.join(ROOT, *a)
ui=open(p('src', 'ui.html'), encoding='utf-8').read()
eng=open(p('src', 'engine.js'), encoding='utf-8').read(); sto=open(p('src', 'story.js'), encoding='utf-8').read()
sheet=base64.b64encode(open(p('art', 'sheet.png'), 'rb').read()).decode(); idx=open(p('art', 'sheet.json'), encoding='utf-8').read(); busts=open(p('art', 'busts.json'), encoding='utf-8').read()
UIMAP={'⏩':'u_fast','⏭':'u_fast','♾':'u_spark','✂':'u_cut','✅':'u_check','✋':'i_tebukuro','✓':'u_check','✨':'u_spark','🌌':'koryu','🌠':'u_spark','🍃':'seed','🍴':'u_eat','🍽':'u_eat','🎁':'u_gift','🎉':'kusudama','🎒':'u_bag','🎞':'u_book','🏅':'u_trophy','🏘':'u_house','🏚':'u_house','🏠':'u_house','🏦':'i_kinchaku','👜':'i_kinchaku','💨':'u_puff','💪':'oni','💴':'coin','📅':'u_daily','📖':'u_book','📗':'u_book','📚':'u_book','🔁':'u_reroll','🔄':'u_reroll','🔇':'u_mute','🔊':'u_sound','🔧':'mallet','🔴':'u_crown','🔵':'u_crown','🗓':'u_daily','😈':'u_curse','🛍':'u_gift','🟠':'u_crown','🟢':'u_crown','🤑':'coin','🧱':'castle','🌫':'c_fog','🔒':'u_lock','🖼':'u_picture','📲':'u_house'}
out=ui.replace('/*__ENGINE__*/',eng).replace('/*__STORY__*/',sto).replace('/*__SHEET__*/',sheet).replace('/*__SPRIDX__*/',idx).replace('/*__BUSTS__*/',busts).replace('/*__UIMAP__*/',json.dumps(UIMAP,ensure_ascii=False))
open(p('index.html'), 'w', encoding='utf-8').write(out)
print(len(out)//1024,'KB')
# ランキングサーバー（worker/）用に、同じエンジンを ES モジュールとして書き出す
names = ['act', 'exportDaily', 'importDaily', 'stepDaily', 'replayDaily', 'newDaily', 'dailySetup', 'setRng', 'SYM', 'ITEMS', 'CURSES', 'DIFFS']
open(p('worker', 'src', 'engine.js'), 'w', encoding='utf-8').write('// tools/build.py が src/engine.js から作るファイル。直接編集しない\n' + eng + '\nexport default { ' + ', '.join(names) + ' };\n')
print('worker/src/engine.js')
