# -*- coding: utf-8 -*-
from flask import Flask, render_template, request

import datetime
import pandas as pd
import numpy as np
import json

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    methodType = ""
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        # 수업 데이터
        with open("../Review.txt", "r", encoding="utf8") as f:
            contents = f.read() # string 타입
            json_data = json.loads(contents)
            
        # 키워드 데이터
        data = pd.read_csv('../keyword.csv', engine='python')
        
        creditString = request.form['credit']
        completeString = request.form['complete']
        
        subCategory = [
            "ICT입문", "소프트웨어활용", "프로그래밍기초",
            "사회과학", "인문학", "자연과학",
            "리더십",
            "세계관1", "세계관2",
            "소통", "융복합",
            "기독교신앙의기초1", "기독교신앙의기초2",
            "Level1", "Level2","Level3", "Remedial", "영어2",
            "스포츠", "예술",
            "제2외국어",
            "전공기초",
            "특론",
        ]

        creditSplit = creditString.split("#")
        remainCredit = []

        for i in range(len(creditSplit)):
            if int(creditSplit[i]) == 0:
                remainCredit.append(subCategory[i])
        
        recommandSection = []
        
        for lectureNum in range(len(json_data)):
            for remainIndex in range(len(remainCredit)):
                if json_data[lectureNum]['subCategory'] == remainCredit[remainIndex]:
                    for sectionNum in range(len(json_data[lectureNum]['sectionList'])):
                        json_data[lectureNum]['sectionList'][sectionNum]['topCategory'] = json_data[lectureNum]['topCategory']
                        json_data[lectureNum]['sectionList'][sectionNum]['subCategory'] = json_data[lectureNum]['subCategory']
                        json_data[lectureNum]['sectionList'][sectionNum]['lectureName'] = json_data[lectureNum]['lectureName']
                        json_data[lectureNum]['sectionList'][sectionNum]['visible'] = False
                        recommandSection.append(json_data[lectureNum]['sectionList'][sectionNum])
                    break

        for index, row in data.iterrows():
            for recommandNum in range(len(recommandSection)):
                if int(recommandSection[recommandNum]['sectionCode']) == int(row[2]):
                    keywords = {"no1": row[4], "no2": row[5], "no3": row[6], "no4": row[7], "no5": row[8]}
                    recommandSection[recommandNum]['keyword'] = keywords
                    break

        sort = sorted(recommandSection, key=(lambda x: x['score']), reverse=True)
        
        
        return render_template('result.html', credit = creditString, remain = remainCredit, recommand = sort)

if __name__ == '__main__':
    app.run(debug=True)
