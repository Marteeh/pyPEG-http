from pypeg2 import *
####################
# MODIFIER CETTE VALEUR POUR TESTER
####################
test_request= \
"""
insérer requete ici
"""

####################
# CODE SOURCE
####################

####################
# DEBUT GRAMMAIRE
####################

#tools

class Digit(int):
    grammar = re.compile(r"[0-9]")

class Number(str):
    grammar = re.compile(r"[0-9]+")

class Alpha(str):
    grammar = re.compile(r"[a-zA-Z]")
    
class HexDig:
    grammar = [Digit, "A", "B", "C", "D", "E", "F"]
    
class SubDelimiter(Keyword):
    grammar = Enum(K("!"), K("$"), K("&"), K("'"), K("("), K(")"), K("*"), K("+"), K(","), K(";"), K("="))
    
class Unreserved(str):
    grammar = [Alpha, Digit, "-", ".", "_", "~"]
    
class PctEncoded:
    grammar = "%", HexDig, HexDig
    
class PChar(str):
    grammar = [Unreserved, PctEncoded, SubDelimiter, ":", "@"]
#endtools

class Method(Keyword):
    grammar = Enum(K("GET"), K("HEAD"), K("POST"), K("PUT"), K("DELETE"), K("TRACE"), K("CONNECT"), K("OPTIONS"))
    
class DecOctet(str):
    grammar = [Digit, (re.compile(r"[1-9]"), Digit), ("1", 2, Digit), ("2", re.compile(r"[0-4]"), Digit), ("25", re.compile(r"[0-5]"))]
    
class IPAddress:
    grammar = attr("ip_field_1", DecOctet), ".", attr("ip_field_2", DecOctet), ".", attr("ip_field_3", DecOctet), ".", attr("ip_field_4", DecOctet)

# reg-name    = ( unreserved | pct-encoded | sub-delims )+
class RegName(str):
    grammar = re.compile(r"([a-zA-Z0-9-._~]|%[A-F0-9])*") 
    
class UserInfo:
    grammar = some([Unreserved, PctEncoded, SubDelimiter, ":"])
    
class Port(str):
    grammar = re.compile(r"[0-9]+")

# obligé de passer par la regex car some considère l'espace
# Segment = *pchar
class Segment(str):
    grammar = re.compile(r"([a-zA-Z0-9-._~:@!$&'()*+,;=]|%[A-F0-9])*") 
    
class Path(List):
    grammar = some("/", Segment)
    
class Authority:
    grammar = optional(attr("userinfo", UserInfo), "@"), attr("host", [IPAddress, RegName]), optional(":", attr("port", Port))

class HierPart:
    grammar = [("//", attr("authority", Authority), optional(attr("path", Path))), attr("path", Path)]
    
class Scheme:
    grammar = Alpha, maybe_some([Alpha, Digit, "+", "-", "."])
    
# obligé de passer par la regex car some considère l'espace
class Query_Fragment(str):
    grammar = re.compile(r"([a-zA-Z0-9-._~/?=]|%[A-F0-9])*") 
    
class URI:
    grammar = attr("scheme", optional(Scheme, ":")), attr("hier_part", HierPart), attr("query", optional("?", Query_Fragment)), attr("fragment", optional("#", Query_Fragment))

class HTTPVersion(str):
    grammar = "HTTP/", Digit, ".", Digit
    
class ReqLine:
    grammar = attr("method", Method), blank, attr("request_uri", URI), blank, attr("http_version", HTTPVersion), endl
    
# token = [^separators]+
class Token(str):
    grammar = re.compile(r"[^()<>@,;:\\\"\/[\]?={}]+")

"""
quoted-string   = <"> *(qdtext) <">
qdtext          = [^"]+
"""
class QuotedString:
    grammar = "\"", re.compile("r[^\"]+"), "\""

"""
qvalue = ( "0" [ "." DIGIT+ ] )
       | ( "1" [ "." "0"+ ]   )
"""
class QValue(str):
    grammar = re.compile(r"(0(\.[0-9]+)?|1((.0)+)?)")

"""
parameter       = attribute "=" value
attribute       = token
value           = token | quoted-string
"""
class Parameter(str):
    grammar = attr("attribute", Token), "=", attr("value", [Token, QuotedString])
    
class Parameters(List):
    grammar = some(Parameter)

class AcceptName(str):
    grammar = re.compile(r"Accept")

# ATTENTION: TROP GOURMAND, ne marche pas
'''
class Accept(str):
    grammar = attr("name", AcceptName), omit(":"), attr("type", Token), "/", attr("subtype", Token), optional(Parameters), attr("q_value", optional(";q=", QValue)), re.compile(r"\n")
'''

# obsolete
class Charset(str):
    grammar = re.compile(r"\w+(-\w+)*"), attr("q_value", optional(";q=", QValue))
    
# RFC 2978
# Je garde que les 3 plus utilisés

class AcceptCharsetName(str):
    grammar = re.compile(r"Accept-Charset")
    
class AcceptCharset(List):
    grammar = attr("name", AcceptCharsetName), omit(":"), csl(Charset)
    
class LanguageRange(str):
    grammar = re.compile(r"\w{1,8}(-\w{1,8})?"), attr("q_value", optional(";q=", QValue))
    
class AcceptLanguageName(str):
    grammar = re.compile(r"Accept-Language")
    
class AcceptLanguage(List):
    grammar = attr("name", AcceptLanguageName), omit(":"), csl(LanguageRange)

class AuthorizationName(str):
    grammar =  re.compile(r"Authorization")
    
class Authorization():
    grammar = attr("name", AuthorizationName), omit(":"), attr("credentials", word)
    
class ContentTypeName(str):
    grammar = re.compile(r"Content-Type")
    
class ContentType:
    grammar = attr("name", ContentTypeName), omit(":"), attr("credentials", (re.compile("[\w-]+"), "/", re.compile("(\w|-)+")))
    
class ContentLengthName(str):
    grammar = re.compile(r"Content-Length")
    
class ContentLength:
    grammar = attr("name", ContentLengthName), omit(":"), attr("value", Number)

class ExpectName(str):
    grammar = re.compile(r"Expect")
    
class Expect(str):
    grammar = attr("name", ExpectName), omit(":"), attr("value", "100-Continue")
    
# basic regex for email

class FromName(str):
    grammar = re.compile(r"From")

class From(str):
    grammar = attr("name", FromName), omit(":"), attr("mailbox", re.compile(r"^[^@\s]+@[^@\s\.]+\.[^@\.\s]+$"))
    
class HostName(str):
    grammar = re.compile(r"Host")

class Host:
    grammar = attr("name", HostName), omit(":"), attr("host", [IPAddress, RegName]), attr("port", optional(":", Port))

class IfMatchName(str):
    grammar = re.compile(r"If-Match")
    
class IfMatch:
    grammar = attr("name", IfMatchName), omit(":"), attr("credentials", word)
    
class ProxyAuthorizationName(Keyword):
    grammar = re.compile(r"Proxy-Authorization")
    
class ProxyAuthorization():
    grammar = attr("name", ProxyAuthorizationName), omit(":"), attr("crendentials", word)
    
class RequestHeader(List):
    grammar = some([AcceptCharset, AcceptLanguage, Authorization, ContentLength, ContentType, Expect, From, Host, IfMatch, ProxyAuthorization])

#END MESSAGE_HEADER

##### REQ
class Request:
    grammar = attr("req_line", ReqLine), endl, attr("request_header", optional(RequestHeader)), endl
#### END REQ

####################
#FIN GRAMMAIRE
####################


# PARSING
f = parse(test_request, Request)

# FONCTION POUR TRADUCTION
def verbalize_req(parsed_request):
    print("Methode: " + parsed_request.req_line.method)
    s = parsed_request.req_line.request_uri.hier_part.path
    print("\nNombre d'élement dans path : " + str(len(s)))

    for i in range(len(s)): 
        print(str(i) + ":\t" + s[i])

    fragment = parsed_request.req_line.request_uri.fragment
    if fragment:
        print("\nFragment: \t" + fragment)
    else:
        print("\nPas de fragment.")

    query = parsed_request.req_line.request_uri.query
    if query:
        print("Query: \t\t"    + query)
    else:
        print("Pas de query.")

    print("\nVersion HTTP: " + parsed_request.req_line.http_version)

    headers = parsed_request.request_header
    print("\nNombre de headers: " + str(len(headers)))
    for i in range(len(headers)):
        print(str(i) + ":\t",  end='')
        header_name = headers[i].name
        print(header_name)
        # Accept trop gourmand, on commence par Accept Charset
        if header_name=="Accept-Charset":
            for j in range(len(headers[i])):
                print("\t--- " + headers[i][j], end=' ')
                if headers[i][j].q_value:
                    print("| q précisé, valeur= " + headers[i][j].q_value, end="")
                print("\n",end="")
                
        elif header_name=="Accept-Language":
            for j in range(len(headers[i])):
                print("\t--- " + headers[i][j], end=' ')
                if headers[i][j].q_value:
                    print("| q précisé, valeur= " + headers[i][j].q_value, end="")
                print("\n",end="")
                
        elif header_name=="Authorization":
            print("\t--- ", headers[i].credentials)
            
        elif header_name=="Content-Length":
            print("\t--- ", headers[i].value)
            
        elif header_name=="Content-Type":
            print("\t--- ", headers[i].credentials)
            
        elif header_name=="Expect":
            print("\t--- 100-continue")
            
        elif header_name=="From":
            print("\t--- " + headers[i].mailbox)
            
        elif header_name=="Host":
            print("\t--- " + headers[i].host, end=' ')
            if headers[i].port:
                print("Port: " + headers[i].port, end=' ')
            print("")
            
        elif header_name=="If-Match":
            print("\t--- " + headers[i].credentials)
            
        elif header_name=="Proxy-Authorization":
            print("\t--- " + headers[i].credentials)

# AFFICHAGE TRAD
verbalize_req(f)
# FIN