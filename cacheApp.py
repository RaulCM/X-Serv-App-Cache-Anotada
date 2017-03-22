#!/usr/bin/python3

import webapp
import urllib.request


class cacheApp (webapp.webApp):

    cache = {}

    def parse(self, request):
        lista = request.split()
        method = lista[0]
        resourceName = lista[1][1:]
        return (method, resourceName)

    def process(self, parsed):

        method, resourceName = parsed

        if method == "GET":
            print(resourceName)
            if resourceName.split("/")[0] == "reload":
                url = resourceName.split("/")[1]
                url = "http://" + url
                httpCode = "302"
                htmlBody = ("<meta http-equiv='refresh' content=3;url=" +
                            url + ">")
            else:
                try:
                    if resourceName in self.cache:
                        httpCode = "200 OK"
                        htmlBody = self.cache[resourceName]
                    else:
                        url = "http://" + resourceName
                        f = urllib.request.urlopen(url)
                        body = f.read().decode('utf-8')
                        self.cache[resourceName] = body
                        before = body.find("<body")
                        after = body.find(">", before)
                        links = ("<a href=" + url + ">Página original</a>" +
                                   "<a href=/reload/" + resourceName +
                                   "> Reload </a>")
                        httpCode = "200 OK"
                        htmlBody = (body[:after + 1] + links +
                                    body[after + 1:])
                except urllib.error.URLError:
                    httpCode = "404 Not Found"
                    htmlBody = "No se ha introducido ninguna URL"
                except UnicodeDecodeError:
                    httpCode = "404 Not Found"
                    htmlBody = "Error al decodificar"
        else:
            httpCode = "HTTP/1.1 405 Method Not Allowed"
            hmtlBody = "method distinto de GET."

        return (httpCode, htmlBody)

if __name__ == "__main__":
    try:
        testWebApp = cacheApp("localhost", 1234)
    except KeyboardInterrupt:
        print("Closing binded socket")
