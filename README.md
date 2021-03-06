# Full Grammar - following RFC 2616 & 3986:

## General format (request or response)

    generic-message =   start-line
                        *(message-header CRLF)
                        CRLF
                        [ message-body ]
    start-line      =   Request-Line | Status-Line
    message-header  =   field-name ":" [ field-value ]
    field-name      =   token
    field-content   =   the OCTETs making up the field-value and consisting of either *TEXT or combinations of token, separators, and quoted-string

## Request format

The request defines the action to be applied to a specified ressource, its identifier and used protocol

    Request             = Request-Line              
                          *(( general-header        
                            | request-header         
                            | entity-header ) CRLF) 
                          CRLF
                          [ message-body ]

SP = space character (' ') and CRLF being the combination of Carriage Return and Line Feed, indicating newline.

### First line

    Request-Line        =   Method SP Request-URI SP HTTP-Version CRLF

The method field indicates what action has to be done with the resource following (Request URI). Case-sensitive.

    Method              =   "OPTIONS"                
                        |   "GET"                    
                        |   "HEAD"                   
                        |   "POST"                   
                        |   "PUT"                    
                        |   "DELETE"                                      
                        |   "TRACE"                  
                        |   "CONNECT"


"The generic URI syntax consists of a hierarchical sequence of components referred to as the scheme, authority, path, query, and fragment."
The URI format described by RFC 3986 is very generic and I chose to simplify it for this project. The structure I respected is the following.

    URI         = [scheme ":"] hier-part [ "?" query ] [ "#" fragment ]

When authority is present, the path must either be empty or begin with a slash ("/" character. When authority is not present, the path cannot begin with two slash characters ("//").
Simplified all other paths types to a single "path" type which is described later on.  

    hier-part   = "//" authority [ path ]
                | "/" path

"Scheme names consist of a sequence of characters beginning with a letter and followed by any combination of letters, digits, plus ("+"), period ("."), or hyphen ("-")."

    scheme      = ALPHA *( ALPHA | DIGIT | "+" | "-" | "." )

Some tools before getting into the rest.

    ALPHA       = [a-zA-Z]
    DIGIT       = [0-9]
    SP          = [ ]
    <">         = ["]
	HEXDIG 		= DIGIT |"A" | "B" | "C" | "D" | "E" | "F"

#### _Authority_
Authority model from the original documentation

    authority   = [ userinfo "@" ] host [ ":" port ]

	userinfo	= ( unreserved | pct-encoded | sub-delims | ":" )+
	
Removed the IPLeteral optional field, mainly consisting of IPv6 implementation. 

    host        = IPv4address | reg-name
    
    reg-name    = ( unreserved | pct-encoded | sub-delims )+
    IPv4address = dec-octet "." dec-octet "." dec-octet "." dec-octet

**%x31-39** and similar following field should be understood as "digit between 1 and 9" (0 and 4; 0 and 5 respectively), being percentage-encoded characters. "A percent-encoded octet is encoded as a character triplet, consisting of the percent character "%" followed by the two hexadecimal digits representing that octet's numeric value."

    dec-octet   = DIGIT               ; 0-9
                | %x31-39 DIGIT       ; 10-99
                | "1" DIGIT{2}        ; 100-199
                | "2" %x30-34 DIGIT   ; 200-249
                | "25" %x30-35        ; 250-255

"The query component contains non-hierarchical data that, along with data in the path component, serves to identify a resource within the scope of the URI's scheme and naming authority."

    query/framgment	= *( pchar 
					   | "/" 
					   | "?" )
"The fragment identifier component of a URI allows indirect identification of a secondary resource by reference to a primary resource and additional identifying information."

    

    pchar       = unreserved | pct-encoded | sub-delims | ":" | "@"
    
    unreserved  = ALPHA | DIGIT | "-" | "." | "_" | "~"
	pct-encoded = "%" HEXDIG{2}
    sub-delims  = "!" | "$" | "&" | "'" | "(" | ")" | "*" | "+" | "," | ";" | "="

#### _Path_
"The path component contains data, usually organized in hierarchical form, that, along with data in the non-hierarchical query component."
"The path is terminated by the first question mark ("?") or number sign ("#") character, or by the end of the URI."
Very generalized path format compared to RFC 3986's format. I considered a mix between path-abempty and path-rootless: the path can begin by "/" or a segment, and is then a succession of segments. 

    path    = *( "/"  segment)

    segment = *pchar

#### HTTP Version

"The version of an HTTP message is indicated by an HTTP-Version field in the first line of the message." (RFC 2145 for knowing version usage)

       HTTP-Version   = "HTTP" "/" DIGIT+ "." DIGIT+

### Message Header

An HTTP request header is the combination of general-, request- and entity- headers, each type being a category of messages.
Giving the large number of possible header messages, I decided to only deal with request headers for this project

#### _request-header_

"The request-header fields allow the client to pass additional information about the request, and about the client itself, to the server."

    request-header      = Accept                   
                        | Accept-Charset           
                        | Accept-Language          
                        | Authorization            
                        | Expect                   
                        | From                     
                        | Host                     
                        | If-Match                 
                        | Proxy-Authorization

These tools will be useful for the following definitions:

    separators      = "(" | ")" | "<" | ">" | "@"
                    | "," | ";" | ":" | "\" | <">
                    | "/" | "[" | "]" | "?" | "="
                    | "{" | "}" |

    token           = [^separators]+

    quoted-string   = <"> *(qdtext) <">
    qdtext          = [^"]+
    
"Quality factors allow the user or user agent to indicate the relative degree of preference for that media-range, using the qvalue scale from 0 to 1".

    qvalue          = ( "0" [ "." DIGIT+ ] )
                    | ( "1" [ "." "0"+ ] )

- *Accept*: "Informs the server about the types of data that can be sent back". For simplicity, I decided that the format of the Accept would be type/subtype.

        Accept      	= "Accept" ":" type "/" subtype *(parameter) [accept-params]

        type            = token
        subtype         = token

        parameter       = attribute "=" value
        attribute       = token
        value           = token | quoted-string

        accept-params   = ";" "q" "=" qvalue 

- *Accept-Charset*: used to indicate what character sets are acceptable for the response.
"If no Accept-Charset header is present, the default is that any character set is acceptable." the `*` character matches every character set. 

        Accept-Charset  = "Accept-Charset" ":"
                          ( ( charset | "*" )[ accept-params ] )*

- *Accept-Language*: Similar to Accept. Informs the server of what is expected to be sent back. Quality value can be associated.

        Accept-Language = "Accept-Language" ":"
                          ( language-range [ accept-params ] )*
        language-range  = ( ALPHA{,8} ("-" ALPHA{,8}) )

- *Authorization*: Contains the credentials to authenticate a user-agent with a server. I assumed that only the "Basic" authentication is used. With this method, the `credentials` field are constructed from the combination of the password and username, encoded with base64 (no encryption, reversible).
        
        Authorization   = "Authorization" ":" credentials
        credentials     = [\w+]

- *Expect*: Indicates expectations that need to be fulfilled by the server to properly handle the request. For example, a client can send a request with a header that indicates a large body, and wait for a 100-continue to send it. I decided not to deal with expectations extensions.

        Expect                  = "Expect" ":" expectation
        expectation             = "100-continue"


- *From*:

   The From request-header field, if given, SHOULD contain an Internet
   e-mail address for the human user who controls the requesting user
   agent. The address SHOULD be machine-usable.

       From   = "From" ":" mailbox

   An example is:

       From: webmaster@w3.org



- *Host*: 

   The Host request-header field specifies the Internet host and port number of the resource being requested. "The Host field value MUST represent the naming authority of the origin server or gateway given by the original URL". 

        Host = "Host" ":" host [ ":" port ]
    
    A "host" without any port specified implies the default port for the requested service (80 for HTTP, for example).
    An example request using the Host field would be:

            GET /pub/WWW/ HTTP/1.1
            Host: www.w3.org

    This field is important as a client MUST include a Host header field in all HTTP/1.1 request messages

- *If-Match* 

    This field is used with a method to make it conditionnal. The purpose of this feature is to update cached information. The special case "*" matches any current entity of the ressource. For GET and HEAD methods, the server will send back the requested resource ONLY if it matches one of the listed tags.

        If-Match = "If-Match" ":" (entity-tag)*

    "Entity tags are used for comparing two or more entities from the samerequested resource." String of ASCII characters surrounded by double quotes (e.g. "67ab43"). It is indicated as weak if prefixed with W/, which means it represents the resource semantically but not byte-for-byte. 

    Example of usage : 

        If-Match: "xyzzy"
        If-Match: "xyzzy", "r2d2xxxx", "c3piozzzz"
        If-Match: *

- *Proxy-Authorization*

    This header allows the client to identify itself to a proxy that requires authentification. 

        Proxy-Authorization     = "Proxy-Authorization" ":" credentials