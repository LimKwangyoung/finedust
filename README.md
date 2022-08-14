# 메타버스 기반 항만 대기오염 모니터링 시스템
## Dataset
- [에어코리아](https://www.airkorea.or.kr)에서 부산광역시의 최종확정 측정자료 사용.
- 부산광역시 항만 측정소 (부산북항)의 측정자료는 측정소가 늦게 설치되어 2018년 11월 이전의 자료는 존재하지 않음.
- 따라서 부산북항과 가까운 부산광역시 동구 초량동 측정소 (부산동구 중앙대로349번길 14)의 측정자료 사용.
- 측정자료는 2012년부터 2021년까지 10년 동안의 PM10, SO2, CO, O3, NO2 수치값 사용.

## dataloader.py
- 에어코리아에서 다운로드 받은 xlsx 또는  csv 파일을 일별로 통합하여 하나의 final.csv로 만듦.
### create_csv
- 최종확정 측정자료로부터 초량동 측정소의 xlsx 또는 csv 파일을 읽어 별도의 csv 파일로 저장.
- 시간별로 수치값이 정렬되어 있으며 Nan이나 -999와 같이 측정되지 않은 값이 존재.
- csv_file 폴더에 저장.
### merge_by_day
- 시간별로 정렬되어 있는 csv 파일 (csv_data)을 일별로 통합하여 별도의 csv 파일로 저장.
- 통합값은 해당 날짜 값의 평균냄.
- 날짜에 Nan 또는 -999와 같이 측정되지 않은 값이 존재할 경우, 해당 날짜를 제외.
- new_csv_file 폴더에 저장.
### concatenate_csv_file
- new_csv_file 폴더의 csv 파일을 통합.
- final.csv 파일로 저장.
### How to use
- 다운로드 받은 파일의 경로를 input_path에 입력.
- final.csv를 만들고자 하는 경로를 output_path에 입력.
- 데이터의 년도를 years에 입력.

## Reference
[파이썬 - 예측모델(LSTM 모델 주가예측](https://post.naver.com/viewer/postView.nhn?volumeNo=29132930&memberNo=18071586)  
[LSTM을 활용한 주식가격 예측](https://dschloe.github.io/python/python_edu/07_deeplearning/deep_learning_lstm/)