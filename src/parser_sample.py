"""
Premier jet pour le parser
Suivant la doc pyPEG et README
"""

from pypeg2 import *

# Il reste a implémenter extension-method --> à voir
# Enum ne marche qu'avec des keywords
class Mehod(Keyword):
    grammar = Enum(K("GET"), K("HEAD"), K("POST"), K("PUT"), K("DELETE"), K("TRACE"), K("CONNECT"), K("OPTIONS"))

class Digit:
    grammar = re.comile(r"[0-9]")

class SubDelimiter(Keyword):
    grammar = Enum(K("!"), K("$"), K("&"), K("'"), K("("), K(")"), K("*"), K("+"), K(","), K(";"), K("="))

# Alpha | Digit 
#   <=> [a-zA-Z0-9_] 
#   <=> \w
class Unreserverd:
    grammar = [re.compile(r"\w"), "-", ".", "_", "~"]

# Pour host, on ignore pct-encoded
class RegularName:
    grammar = maybe_some([Unreserved, SubDelimiter]) 

#Je decide de skip pct-encoded pour l'instant
class PChar:
    grammar = [Unreserved, SubDelimiter, ":", "@"]

#Start Authority
class Fragment:
    grammar = maybe_some([PChar, "/", "?"])

class DecOctet:
    grammar = [Digit, ([1-9], Digit), ("1", Digit, Digit), ("2", [0-4], Digit), ("25", [0-5])]

# Not considering IPv6 adresses for the moment
class IPAddr:
    grammar = DecOctet, ".", DecOctet, ".", DecOctet, ".", DecOctet

class Host:
    grammar = [IPAddr, RegularName]

class Port:
    grammar = maybe_some(Digit)

class Authority:
    grammar = Host, maybe_some(":", Port)
# end Authority

#start Path
class Segment:
    grammar = maybe_some(PChar)
class Path:
    grammar = Segment, maybe_some("/", Segment)
#end Path
class HierPArt:
    grammar = "//" Authority Path

#TODO: changer cette expreg (marche pas)
class RequestURI:
    grammar = re.compile(r"^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?")

class HttpVer

class ReqLine:
    grammar = attr("method", Method), whitespace, attr("request_uri", RequestURI), whitespace, attr("http_version", HttpVer), endl

class Request:
    grammar = attr("req_line", ReqLine), maybe_some(attr("header", Header), endl), endl, optional(attr("mess_body", MessageBody))