"""
Author: COMP90024 Group 32, 2024 May
    Yucheng Luo     <1153247>  <stluo@student.unimelb.edu.au>
    Yiyang Huang    <1084743>  <yiyahuang@student.unimelb.edu.au>
    Jiaqi Fan       <1266359>  <jffan2@student.unimelb.edu.au>
    Yingying Zhong  <1158586>  <yizhong1@student.unimelb.edu.au>
    Mingyao Ke      <1240745>  <mingyaok@student.unimelb.edu.au>
"""


from elasticsearch8 import Elasticsearch

class Utils:
    @staticmethod
    def config(k):
        with open(f'/configs/default/parameters/{k}', 'r') as f:
            return f.read()
        
    @staticmethod
    def secret(k):
        with open(f'/secrets/default/secret/{k}', 'r') as f:
            return f.read()
    
    @staticmethod
    def get_es_client():
        client = Elasticsearch (
            Utils.config("ES_URL"),
            verify_certs= False,
            ssl_show_warn= False,
            basic_auth=(Utils.secret("es_username"), Utils.secret("es_password"))
        )
        return client

    @staticmethod
    def get_weather_api():
        return {
            "tMAL-station-charlton": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94839.json", 
            "tMAL-station-hopetoun-airport": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94838.json", 
            "tMAL-station-kerang": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94844.json", 
            "tMAL-station-mildura": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94693.json", 
            "tMAL-station-swan-hill": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94843.json", 
            "tMAL-station-walpeup": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95831.json", 
            "tWIM-station-edenhope": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95832.json", 
            "tWIM-station-horsham": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95839.json", 
            "tWIM-station-kanagulk": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95827.json", 
            "tWIM-station-longerenong": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95835.json", 
            "tWIM-station-nhill-aerodrome": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94827.json", 
            "tWIM-station-stawell": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94836.json", 
            "tWIM-station-warracknabeal-airport": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94920.json", 
            "tSW-station-ararat": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94834.json", 
            "tSW-station-ben-nevis": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94835.json", 
            "tSW-station-casterton": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95825.json", 
            "tSW-station-dartmoor": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95822.json", 
            "tSW-station-hamilton": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94829.json", 
            "tSW-station-mortlake": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94840.json", 
            "tSW-station-mount-gellibrand": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95845.json", 
            "tSW-station-mount-william": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94833.json", 
            "tSW-station-portland-airport": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94828.json", 
            "tSW-station-portland-harbour": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95826.json", 
            "tSW-station-warrnambool": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94837.json", 
            "tSW-station-westmere": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95840.json", 
            "tCEN-station-avalon": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94854.json", 
            "tCEN-station-ballarat": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94852.json", 
            "tCEN-station-cerberus": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94898.json", 
            "tCEN-station-coldstream": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94864.json", 
            "tCEN-station-essendon-airport": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95866.json", 
            "tCEN-station-ferny-creek": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94872.json", 
            "tCEN-station-frankston-ballam-park": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94876.json", 
            "tCEN-station-geelong-racecourse": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94857.json", 
            "tCEN-station-laverton": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94865.json", 
            "tCEN-station-melbourne-airport": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94866.json", 
            "tCEN-station-melbourne-olympic-park": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95936.json", 
            "tCEN-station-moorabbin-airport": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94870.json", 
            "tCEN-station-point-cook": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95941.json", 
            "tCEN-station-pound-creek": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94886.json", 
            "tCEN-station-scoresby": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95867.json", 
            "tCEN-station-sheoaks": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94863.json", 
            "tCEN-station-st-kilda-harbour-rmys": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95864.json", 
            "tCEN-station-viewbank": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95874.json", 
            "tCEN-station-wonthaggi": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95881.json", 
            "tNCY-station-bendigo": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94855.json", 
            "tNCY-station-echuca": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94861.json", 
            "tNCY-station-kyabram": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95833.json", 
            "tNCY-station-mangalore": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94874.json", 
            "tNCY-station-redesdale": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94859.json", 
            "tNCY-station-shepparton": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94875.json", 
            "tNCY-station-strathbogie": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95843.json", 
            "tNCY-station-tatura": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95836.json", 
            "tNCY-station-yarrawonga": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94862.json", 
            "tNE-station-albury": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95896.json", 
            "tNE-station-benalla": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94884.json", 
            "tNE-station-falls-creek": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94903.json", 
            "tNE-station-hunters-hill": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94878.json", 
            "tNE-station-lake-dartmouth": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94888.json", 
            "tNE-station-mount-buller": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94894.json", 
            "tNE-station-mount-hotham-airport": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94905.json", 
            "tNE-station-mount-hotham": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94906.json", 
            "tNE-station-rutherglen": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95837.json", 
            "tNE-station-wangaratta": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94889.json", 
            "tNC-station-castlemaine": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95853.json", 
            "tNC-station-eildon-fire-tower": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94881.json", 
            "tNC-station-kilmore-gap": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94860.json", 
            "tNC-station-lake-eildon": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94882.json", 
            "tNC-station-maryborough": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94849.json", 
            "tNC-station-puckapunyal-lyon-hill-defence": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94858.json", 
            "tNC-station-puckapunyal-west-defence": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94856.json", 
            "tWSG-station-east-sale-airport": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95907.json", 
            "tWSG-station-latrobe-valley": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94891.json", 
            "tWSG-station-mount-baw-baw": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95901.json", 
            "tWSG-station-mount-moornapa": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95913.json", 
            "tWSG-station-warragul-nilma-north": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.99806.json", 
            "tWSG-station-wilsons-promontory": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94893.json", 
            "tWSG-station-yanakie": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94911.json", 
            "tWSG-station-yarram-airport": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95890.json", 
            "tEG-station-bairnsdale": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94912.json", 
            "tEG-station-combienbar": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94914.json", 
            "tEG-station-gelantipy": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94913.json", 
            "tEG-station-mallacoota": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94935.json", 
            "tEG-station-mount-nowa-nowa": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94930.json", 
            "tEG-station-omeo": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.94908.json", 
            "tEG-station-orbost": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.95918.json", 
            "tPORT-station-victoria-portable-aws-a-cfa": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.99813.json", 
            "tPORT-station-wycheprooof-cfa": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.99815.json", 
            "tPORT-station-victoria-portable-aws-d-cfa": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.99816.json", 
            "tPORT-station-victoria-portable-aws-g-cfa": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.99819.json", 
            "tPORT-station-portable-vpha-delwp": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.99795.json", 
            "tPORT-station-portable-vphc-delwp": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.99809.json", 
            "tPORT-station-portable-vphd-delwp": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.99810.json", 
            "tPORT-station-portable-vphe-delwp": "https://reg.bom.gov.au//fwo/IDV60801/IDV60801.99811.json"
        }
        
        
    @staticmethod
    def get_site_sa2():
        return [
            {"site": "tMAL-station-charlton", "sa2_code": "215031400", "sa2_name": "Buloke", "location": [143.3, -36.3]}, 
            {"site": "tMAL-station-hopetoun-airport", "sa2_code": "215011394", "sa2_name": "Yarriambiack", "location": [142.4, -35.7]}, 
            {"site": "tMAL-station-kerang", "sa2_code": "215031402", "sa2_name": "Kerang", "location": [143.9, -35.7]}, 
            {"site": "tMAL-station-mildura", "sa2_code": "215021470", "sa2_name": "Mildura - South", "location": [142.1, -34.2]}, 
            {"site": "tMAL-station-swan-hill", "sa2_code": "215031404", "sa2_name": "Swan Hill", "location": [143.5, -35.4]}, 
            {"site": "tMAL-station-walpeup", "sa2_code": "215021398", "sa2_name": "Mildura Surrounds", "location": [142.0, -35.1]}, 
            {"site": "tWIM-station-edenhope", "sa2_code": "215011393", "sa2_name": "West Wimmera", "location": [141.3, -37.0]}, 
            {"site": "tWIM-station-horsham", "sa2_code": "215011388", "sa2_name": "Horsham", "location": [142.2, -36.7]}, 
            {"site": "tWIM-station-kanagulk", "sa2_code": "215011389", "sa2_name": "Horsham Surrounds", "location": [141.8, -37.1]}, {"site": "tWIM-station-longerenong", "sa2_code": "215011389", "sa2_name": "Horsham Surrounds", "location": [142.3, -36.7]}, {"site": "tWIM-station-nhill-aerodrome", "sa2_code": "215011390", "sa2_name": "Nhill Region", "location": [141.6, -36.3]}, {"site": "tWIM-station-stawell", "sa2_code": "215011392", "sa2_name": "Stawell", "location": [142.7, -37.1]}, {"site": "tWIM-station-warracknabeal-airport", "sa2_code": "215011394", "sa2_name": "Yarriambiack", "location": [142.4, -36.3]}, {"site": "tSW-station-ararat", "sa2_code": "215011387", "sa2_name": "Ararat Surrounds", "location": [143.0, -37.3]}, {"site": "tSW-station-ben-nevis", "sa2_code": "201031013", "sa2_name": "Avoca", "location": [143.2, -37.2]}, {"site": "tSW-station-casterton", "sa2_code": "217011420", "sa2_name": "Glenelg (Vic.)", "location": [141.3, -37.6]}, {"site": "tSW-station-dartmoor", "sa2_code": "217011420", "sa2_name": "Glenelg (Vic.)", "location": [141.3, -37.9]}, {"site": "tSW-station-hamilton", "sa2_code": "217011423", "sa2_name": "Southern Grampians", "location": [142.1, -37.6]}, {"site": "tSW-station-mortlake", "sa2_code": "217041477", "sa2_name": "Moyne - East", "location": [142.8, -38.1]}, {"site": "tSW-station-mount-gellibrand", "sa2_code": "217031473", "sa2_name": "Colac Surrounds", "location": [143.8, -38.2]}, {"site": "tSW-station-mount-william", "sa2_code": "215011387", "sa2_name": "Ararat Surrounds", "location": [142.6, -37.3]}, {"site": "tSW-station-portland-airport", "sa2_code": "217011420", "sa2_name": "Glenelg (Vic.)", "location": [141.5, -38.3]}, {"site": "tSW-station-portland-harbour", "sa2_code": "217011420", "sa2_name": "Glenelg (Vic.)", "location": [141.6, -38.3]}, {"site": "tSW-station-warrnambool", "sa2_code": "217041477", "sa2_name": "Moyne - East", "location": [142.5, -38.3]}, {"site": "tSW-station-westmere", "sa2_code": "215011387", "sa2_name": "Ararat Surrounds", "location": [142.9, -37.7]}, {"site": "tCEN-station-avalon", "sa2_code": "203021043", "sa2_name": "Lara", "location": [144.5, -38.0]}, {"site": "tCEN-station-ballarat", "sa2_code": "201011008", "sa2_name": "Wendouree - Miners Rest", "location": [143.8, -37.5]}, {"site": "tCEN-station-cerberus", "sa2_code": "214021379", "sa2_name": "Hastings - Somers", "location": [145.2, -38.4]}, {"site": "tCEN-station-coldstream", "sa2_code": "211051278", "sa2_name": "Lilydale - Coldstream", "location": [145.4, -37.7]}, {"site": "tCEN-station-essendon-airport", "sa2_code": "210031439", "sa2_name": "Gowanbrae", "location": [144.9, -37.7]}, {"site": "tCEN-station-ferny-creek", "sa2_code": "211011448", "sa2_name": "Ferntree Gully (South) - Upper Ferntree Gully", "location": [145.3, -37.9]}, {"site": "tCEN-station-frankston-ballam-park", "sa2_code": "214021385", "sa2_name": "Somerville", "location": [145.2, -38.2]}, {"site": "tCEN-station-geelong-racecourse", "sa2_code": "203021045", "sa2_name": "Newcomb - Moolap", "location": [144.4, -38.2]}, {"site": "tCEN-station-laverton", "sa2_code": "213051464", "sa2_name": "Point Cook - East", "location": [144.8, -37.9]}, {"site": "tCEN-station-melbourne-airport", "sa2_code": "213011340", "sa2_name": "Taylors Lakes", "location": [144.8, -37.7]}, {"site": "tCEN-station-melbourne-olympic-park", "sa2_code": "206071139", "sa2_name": "Abbotsford", "location": [145.0, -37.8]}, {"site": "tCEN-station-moorabbin-airport", "sa2_code": "208031193", "sa2_name": "Mordialloc - Parkdale", "location": [145.1, -38.0]}, {"site": "tCEN-station-point-cook", "sa2_code": "213051464", "sa2_name": "Point Cook - East", "location": [144.8, -37.9]}, {"site": "tCEN-station-pound-creek", "sa2_code": "205031093", "sa2_name": "Wonthaggi - Inverloch", "location": [145.8, -38.6]}, {"site": "tCEN-station-scoresby", "sa2_code": "211011448", "sa2_name": "Ferntree Gully (South) - Upper Ferntree Gully", "location": [145.3, -37.9]}, {"site": "tCEN-station-sheoaks", "sa2_code": "203011035", "sa2_name": "Golden Plains - South", "location": [144.1, -37.9]}, {"site": "tCEN-station-st-kilda-harbour-rmys", "sa2_code": "208011169", "sa2_name": "Brighton (Vic.)", "location": [145.0, -37.9]}, {"site": "tCEN-station-viewbank", "sa2_code": "209011197", "sa2_name": "Greensborough", "location": [145.1, -37.7]}, {"site": "tCEN-station-wonthaggi", "sa2_code": "205031093", "sa2_name": "Wonthaggi - Inverloch", "location": [145.6, -38.6]}, {"site": "tNCY-station-bendigo", "sa2_code": "202011025", "sa2_name": "White Hills - Ascot", "location": [144.3, -36.7]}, {"site": "tNCY-station-echuca", "sa2_code": "216011406", "sa2_name": "Echuca", "location": [144.8, -36.2]}, {"site": "tNCY-station-kyabram", "sa2_code": "216011407", "sa2_name": "Kyabram", "location": [145.1, -36.3]}, {"site": "tNCY-station-mangalore", "sa2_code": "204011058", "sa2_name": "Nagambie", "location": [145.2, -36.9]}, {"site": "tNCY-station-redesdale", "sa2_code": "202021028", "sa2_name": "Castlemaine Surrounds", "location": [144.5, -37.0]}, {"site": "tNCY-station-shepparton", "sa2_code": "216031594", "sa2_name": "Shepparton - South East", "location": [145.4, -36.4]}, {"site": "tNCY-station-strathbogie", "sa2_code": "204011055", "sa2_name": "Euroa", "location": [145.7, -36.8]}, {"site": "tNCY-station-tatura", "sa2_code": "216031419", "sa2_name": "Shepparton Surrounds - West", "location": [145.3, -36.4]}, {"site": "tNCY-station-yarrawonga", "sa2_code": "109031181", "sa2_name": "Corowa Surrounds", "location": [146.0, -36.0]}, {"site": "tNE-station-albury", "sa2_code": "204031491", "sa2_name": "Baranduda - Leneva", "location": [147.0, -36.1]}, {"site": "tNE-station-benalla", "sa2_code": "204021063", "sa2_name": "Benalla", "location": [146.0, -36.6]}, {"site": "tNE-station-falls-creek", "sa2_code": "205021082", "sa2_name": "Bruthen - Omeo", "location": [147.3, -36.9]}, {"site": "tNE-station-hunters-hill", "sa2_code": "204031072", "sa2_name": "Towong", "location": [147.5, -36.2]}, {"site": "tNE-station-lake-dartmouth", "sa2_code": "204031072", "sa2_name": "Towong", "location": [147.5, -36.5]}, {"site": "tNE-station-mount-buller", "sa2_code": "204011057", "sa2_name": "Mansfield (Vic.)", "location": [146.4, -37.1]}, {"site": "tNE-station-mount-hotham-airport", "sa2_code": "205021082", "sa2_name": "Bruthen - Omeo", "location": [147.3, -37.0]}, {"site": "tNE-station-mount-hotham", "sa2_code": "204031069", "sa2_name": "Bright - Mount Beauty", "location": [147.1, -37.0]}, {"site": "tNE-station-rutherglen", "sa2_code": "204021065", "sa2_name": "Rutherglen", "location": [146.5, -36.1]}, {"site": "tNE-station-wangaratta", "sa2_code": "204021067", "sa2_name": "Wangaratta Surrounds", "location": [146.3, -36.4]}, {"site": "tNC-station-castlemaine", "sa2_code": "202021027", "sa2_name": "Castlemaine", "location": [144.2, -37.1]}, {"site": "tNC-station-eildon-fire-tower", "sa2_code": "204011054", "sa2_name": "Alexandra", "location": [145.8, -37.2]}, {"site": "tNC-station-kilmore-gap", "sa2_code": "209041224", "sa2_name": "Wallan", "location": [145.0, -37.4]}, {"site": "tNC-station-lake-eildon", "sa2_code": "204011054", "sa2_name": "Alexandra", "location": [145.9, -37.2]}, {"site": "tNC-station-maryborough", "sa2_code": "201031017", "sa2_name": "Maryborough Surrounds", "location": [143.7, -37.1]}, {"site": "tNC-station-puckapunyal-lyon-hill-defence", "sa2_code": "204011060", "sa2_name": "Seymour Surrounds", "location": [145.1, -36.9]}, {"site": "tNC-station-puckapunyal-west-defence", "sa2_code": "204011060", "sa2_name": "Seymour Surrounds", "location": [144.9, -37.0]}, {"site": "tWSG-station-east-sale-airport", "sa2_code": "205051100", "sa2_name": "Longford - Loch Sport", "location": [147.1, -38.1]}, {"site": "tWSG-station-latrobe-valley", "sa2_code": "205041494", "sa2_name": "Traralgon - West", "location": [146.5, -38.2]}, {"site": "tWSG-station-mount-baw-baw", "sa2_code": "205011077", "sa2_name": "Mount Baw Baw Region", "location": [146.3, -37.8]}, {"site": "tWSG-station-mount-moornapa", "sa2_code": "205051099", "sa2_name": "Alps - West", "location": [147.1, -37.7]}, {"site": "tWSG-station-warragul-nilma-north", "sa2_code": "205011079", "sa2_name": "Warragul", "location": [146.0, -38.1]}, {"site": "tWSG-station-wilsons-promontory", "sa2_code": "205031092", "sa2_name": "Wilsons Promontory", "location": [146.4, -39.1]}, {"site": "tWSG-station-yanakie", "sa2_code": "205031087", "sa2_name": "Foster", "location": [146.2, -38.8]}, {"site": "tWSG-station-yarram-airport", "sa2_code": "205051104", "sa2_name": "Yarram", "location": [146.7, -38.6]}, {"site": "tEG-station-bairnsdale", "sa2_code": "205021086", "sa2_name": "Paynesville", "location": [147.6, -37.9]}, {"site": "tEG-station-combienbar", "sa2_code": "205021085", "sa2_name": "Orbost", "location": [149.0, -37.3]}, {"site": "tEG-station-gelantipy", "sa2_code": "205021085", "sa2_name": "Orbost", "location": [148.3, -37.2]}, {"site": "tEG-station-mallacoota", "sa2_code": "205021085", "sa2_name": "Orbost", "location": [149.7, -37.6]}, {"site": "tEG-station-mount-nowa-nowa", "sa2_code": "205021085", "sa2_name": "Orbost", "location": [148.1, -37.7]}, {"site": "tEG-station-omeo", "sa2_code": "205021082", "sa2_name": "Bruthen - Omeo", "location": [147.6, -37.1]}, {"site": "tEG-station-orbost", "sa2_code": "205021085", "sa2_name": "Orbost", "location": [148.5, -37.7]}, {"site": "tPORT-station-victoria-portable-aws-a-cfa", "sa2_code": "217031474", "sa2_name": "Corangamite - North", "location": [143.6, -38.0]}, {"site": "tPORT-station-wycheprooof-cfa", "sa2_code": "215031400", "sa2_name": "Buloke", "location": [143.2, -36.1]}, {"site": "tPORT-station-victoria-portable-aws-d-cfa", "sa2_code": "205051099", "sa2_name": "Alps - West", "location": [146.6, -37.6]}, {"site": "tPORT-station-victoria-portable-aws-g-cfa", "sa2_code": "215021398", "sa2_name": "Mildura Surrounds", "location": [141.3, -35.6]}, {"site": "tPORT-station-portable-vpha-delwp", "sa2_code": "201031013", "sa2_name": "Avoca", "location": [143.3, -37.1]}, {"site": "tPORT-station-portable-vphc-delwp", "sa2_code": "215011392", "sa2_name": "Stawell", "location": [142.4, -37.1]}, {"site": "tPORT-station-portable-vphd-delwp", "sa2_code": "217011423", "sa2_name": "Southern Grampians", "location": [142.3, -37.6]}, {"site": "tPORT-station-portable-vphe-delwp", "sa2_code": "215011387", "sa2_name": "Ararat Surrounds", "location": [142.5, -37.4]}]
