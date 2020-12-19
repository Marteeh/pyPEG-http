"""
Premier jet pour le parser
Suivant la doc pyPEG et README
"""
# Il reste a implémenter extension-method --> à voir
# Enum ne marche qu'avec des keywords
class Mehod(Keyword):
    grammar = Enum(K("GET"), K("HEAD"), K("POST"), K("PUT"), K("DELETE"), K("TRACE"), K("CONNECT"), K("OPTIONS"))

class RequestURI:
    grammar = re.compile(r"^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?")

class HttpVer

class ReqLine:
    grammar = attr("method", Method), whitespace, attr("request_uri", RequestURI), whitespace, attr("http_version", HttpVer), endl

class Request:
    grammar = attr("req_line", ReqLine), maybe_some(attr("header", Header), endl), endl, optional(attr("mess_body", MessageBody))