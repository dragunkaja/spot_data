import pandas as pd
import json

with open('data/raw/Streaming_History_Audio_2018-2019_0.json', 'r', encoding='utf-8') as f:
    streaming_history_2018_2019= json.load(f)
    streaming_history_2018_2019= pd.DataFrame(streaming_history_2018_2019)

