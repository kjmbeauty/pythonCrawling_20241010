import json

import requests
import urllib.request
import datetime
import pandas as pd


# url = 'http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList'
# params ={'serviceKey' : 'cTWUGiJR/GRNsWP1Zvpr6EfojgF2NzRo6pzKHUXZplHewa1M8A9dkuiqnqsbVFTvix8hc8GWw4abmLFx7YB5tA==', 'YM' : '201205', 'NAT_CD' : '130', 'ED_CD' : 'E' }
#
# response = requests.get(url, params=params)
# print(response.text)

def getRequestUrl(url):
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:  # 정상 응답 코드
            print(f"요청에 대한 응답 성공 [{datetime.datetime.now()}]")
            return response.read().decode("utf-8")
    except Exception as e:
        print(e)
        print(f"에러 발생 url : {url} [{datetime.datetime.now()}]")
        return None

def getTourismStatsItem(yyyymm, nat_cd, ed_cd):  # 출입년월, 국가코드, 입국(E)/출국(D)
    url = 'http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList'
    parameters = "?_type=json&serviceKey=cTWUGiJR/GRNsWP1Zvpr6EfojgF2NzRo6pzKHUXZplHewa1M8A9dkuiqnqsbVFTvix8hc8GWw4abmLFx7YB5tA=="
    parameters = parameters + f"&YM={yyyymm}"
    parameters = parameters + f"&NAT_CD={nat_cd}"
    parameters = parameters + f"&ED_CD={ed_cd}"

    url = url + parameters
    responseDecode = getRequestUrl(url)
    print(responseDecode)

    if responseDecode == None:  # 에러 발생 검색 실패
        return None
    else:  # 응답 성공        p
        return json.loads(responseDecode)  # 파이썬에서 처리 가능한 객체로 변환하여 반환

# resultTest = getTourismStatsItem("202005","130","E")
# print(resultTest)

# 시작 년월과 종료 년월을 인수로 넣으면 해당 기간 동안의 출입국 데이터를 가져오는 함수
result = []
jsonResult = []
def getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear):
    for year in range(int(nStartYear), int(nEndYear)+1):
        for month in range(1, 13):
            yyyymm = f"{year}{month:0>2}"
            jsonData = getTourismStatsItem(yyyymm, nat_cd, ed_cd)

            print(yyyymm)

            if jsonData["response"]["body"]["items"] == "":
                print(f"현재 제공되는 통계 데이터는 {year}년 {month-1}월 입니다.")
                # dataEnd = f"{year}{month-1:0>2}"
                break

            natName = jsonData["response"]["body"]["items"]["item"]["natKorNm"]  # 나라 이름
            num = jsonData["response"]["body"]["items"]["item"]["num"]  # 입국자 수
            # natCd = jsonData["response"]["body"]["items"]["item"]["natCd"]  # 국가코드
            jsonResult.append({"nat_name":natName, "nat_cd":nat_cd, "yyyymm":yyyymm, "visit_cnt":num})
            result.append([natName, nat_cd, yyyymm, num])


    return jsonResult

resultTest = getTourismStatsService("130", "E", "2024", "2024")
print(resultTest)
print(result)

# csv 파일로 출력

result_df = pd.DataFrame(result, columns=["입국자국가","국가코드","입국연월","입국자수"])
print(result_df)
result_df.to_csv("2024년_출입국자수.csv", index=False, encoding='cp949')

print("-----")
