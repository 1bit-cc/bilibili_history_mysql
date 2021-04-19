import requests,json,os

class bili(object):

    bi_path = ""
    bi_max = ""
    bi_view_at = ""

    history_list = []

    def __init__(self,path,max,view_at):
        self.bi_path = path
        self.bi_max = max
        self.bi_view_at = view_at

    def get_cookie(self):
        if os.path.exists(self.bi_path+'cookie.txt') == True:
            with open(self.bi_path+'cookie.txt', 'r',encoding='utf-8') as fp:
                cookie = fp.read()
            if cookie != "":
                return {"code":0,"info":"OK","cookie":cookie}
            else:
                return {"code":1,"info":"Empty file","cookie":""}
        else:
            return {"code":1,"info":"File is not present","cookie":""}

    def write_history(self):
        write_data = {"history":self.history_list}
        with open(self.bi_path+"history/history.json", 'w+',encoding='utf-8') as fp:
            fp.write(json.dumps(write_data,indent=4))

    def get_history(self):
        url = "https://api.bilibili.com/x/web-interface/history/cursor?max="+self.bi_max+"&view_at="+self.bi_view_at+"&business=archive"

        print(url)

        headers = {
            "cookie" : self.get_cookie()["cookie"],
            "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66"
        }

        data = json.loads(requests.get(url=url,headers=headers).text)["data"]

        node_max = data["cursor"]["max"]
        node_view_at = data["cursor"]["view_at"]
        node_ps = data["cursor"]["ps"]
        node_list = data["list"]

        if node_max == node_view_at == node_ps == 0 and node_list == []:
            return False
        else:

            self.bi_max = str(node_max)
            self.bi_view_at = str(node_view_at)

            for temp in node_list:
                
                self.history_list.append(temp)

            return True