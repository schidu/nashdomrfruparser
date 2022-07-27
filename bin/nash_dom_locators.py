DATA_OBJECT = {'ID дома':('$.data["id"]',),#,
                "Статус":('$.data["photoRenderDTO"][0]["objReadyDesc"]',),
                'Название':('$.data["nameObj"]',),
                # 'Адрес':('$.data["address"]',),
                'Longitude':('$.data["objLkLongitude"]',),
                'Latitude':('$.data["objLkLatitude"]',),
                'Статус числом':('$.data["objStatus"]',),
                'Застройщик форма':('$.data["developer"]["orgForm"]["shortForm"]',),
                'Застройщик':('$.data["developer"]["devShortCleanNm"]',),
                'Застройщик номер':('$.data["developer"]["devId"]',),
                'Группа компаний':('$.data["developer"]["developerGroupName"]',),
                'Группа компаний номер':('$.data["developer"]["companyGroupId"]',),
                #'ЖК':,
                #'Проектная декларация',
                'Ввод в эксплуатацию':('$.data["objReady100PercDt"]',),
                'Выдача ключей':('$.data["objTransferPlanDt"]',),
                'Средняя цена':('$.data["objPriceAvg"]',),
                'Продажа через эскроу':('$.data["objGuarantyEscrowFlg"]',),
                #'Распроданность квартир',
                'Класс недвижимости':('$.data["objLkClassDesc"]',),
                'Материал стен':('$.data["wallMaterialShortDesc"]',),
                'Тип отделки':('$.data["objLkFinishTypeDesc"]',),
                'Свободная планировка':('$.data["objLkFreePlanDesc"]',),
                'Количество этажей':('$.data["objFloorCnt"]',),
                'Количество квартир':('$.data["objFlatCnt"]',),
                'Жилая площадь':('$.data["objSquareLiving"]',),
                'Высота потолков':('$.data["objLivCeilingHeight"]',),
                #'Велосипедные дорожки',
                #'Количество детских площадок',
                #'Количество спортивных площадок',
                #'Количество площадок',
                'Количество мест в паркинге':('$.data["objElemParkingCnt"]',),
                'Гостевые места на':('$.data["objInfrstrObjPrkngCnt"]',),
                #'Гостевые места вне',
                #'Наличие пандуса',
                #'Наличие понижающих площадок',
                #'Количество инвалидных',
                'Количество подъездов':('$.data["objLivElemCnt"]',),
                'Количество пассажирских':('$.data["objElevatorPassengerCnt"]',),
                'Количество грузовых':('$.data["objElevatorCargoCnt"]',)
}


API_QUERY = 'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/object/{}'
DEVELOPER_LINK = 'https:///xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%B5%D0%B4%D0%B8%D0%BD%D1%8B%D0%B9-%D1%80%D0%B5%D0%B5%D1%81%D1%82%D1%80-%D0%B7%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D1%89%D0%B8%D0%BA%D0%BE%D0%B2/%D0%B7%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D1%89%D0%B8%D0%BA/{}'
BUILDING_TRUST_LINK = 'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%B5%D0%B4%D0%B8%D0%BD%D1%8B%D0%B9-%D1%80%D0%B5%D0%B5%D1%81%D1%82%D1%80-%D0%B7%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D1%89%D0%B8%D0%BA%D0%BE%D0%B2/%D0%B7%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D1%89%D0%B8%D0%BA/{}'

PAGE_PERMITS_QUERY = 'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/object/{}/document/permits'
PAGE_DOCUMENTATION_QUERY ='https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/object/{}/project/documentation'

DATA_PERMITS = {'Разрешение на строительство':('$.data[?(@.typeDoc=="rns")]."docObjRnsIssueDt"',), # name/descriptor/date
        'Экспертиза проектной документации':('$.data[?(@.typeDoc=="proj_expt_result")]."docObjRnsIssueDt"',) # name/descriptor/date
        }

DATA_DOCUMENTATION = {'Градостроительный план земельного участка':('$.data[?(@.typeDoc=="gpzu")]."fileUploadDt"',), # name/descriptor/date
                      'Извещение о начале строительства':('$.data[?(@.typeDoc=="notice_start")]."fileUploadDt"',), # name/descriptor/date
                      'Схема планировочной организации земельного участка':('$.data[?(@.typeDoc=="doc_obj_plan")]."fileUploadDt"',)} # name/descriptor/date
