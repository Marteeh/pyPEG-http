# pyPEG-http
A pyPEG parser for HTTP request/response

**1st step**: Getting used to pyPEG with simple HTTP requests (GET)

## Full Grammar - following RFC 2616 & 3986:

### General format (request or response)

    generic-message =   start-line
                        *(message-header CRLF)
                        CRLF
                        [ message-body ]
    start-line      =   Request-Line | Status-Line
    message-header  =   field-name ":" [ field-value ]
    field-name      =   token
    field-content   =   the OCTETs making up the field-value and consisting of either *TEXT or combinations of token, separators, and quoted-string

### Request format

The request defines the action to be applied to a specified ressource, its identifier and used protocol

    Request             = Request-Line              
                          *(( general-header        
                            | request-header         
                            | entity-header ) CRLF) 
                          CRLF
                          [ message-body ]

SP = space character (' ') and CRLF being the combination of .. and .., indicating newline.

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
                        |   extension-method
    extension-method    = token

"The generic URI syntax consists of a hierarchical sequence of components referred to as the scheme, authority, path, query, and fragment."
The URI format described by RFC 3986 is very generic and I chose to simplify it for this project. The structure I respected is the following.

    URI         = scheme ":" hier-part [ "?" query ] [ "#" fragment ]

Simplified all path types to a single "path" type which is described later on.  

    hier-part   = "//" authority path

"Scheme names consist of a sequence of characters beginning with a letter and followed by any combination of letters, digits, plus ("+"), period ("."), or hyphen ("-")."

    scheme      = ALPHA *( ALPHA | DIGIT | "+" | "-" | "." )

#### _Authority_
Authority model simplified from the original one (not including user info)

    authority   = host [ ":" port ]

Removed the IPLeteral optional, mainly consisting of IPv6 implementation. 

    host        = IPv4address | reg-name
    
    reg-name    = *( unreserved | pct-encoded | sub-delims )
    IPv4address = dec-octet "." dec-octet "." dec-octet "." dec-octet

**%x31-39** and similar following field should be understood as "digit between 1 and 9" (0 and 4; 0 and 5 respectively), being percentage-encoded characters. "A percent-encoded octet is encoded as a character triplet, consisting of the percent character "%" followed by the two hexadecimal digits representing that octet's numeric value."

    dec-octet   = DIGIT               ; 0-9
                | %x31-39 DIGIT       ; 10-99
                | "1" DIGIT{2}        ; 100-199
                | "2" %x30-34 DIGIT   ; 200-249
                | "25" %x30-35        ; 250-255

"The query component contains non-hierarchical data that, along with data in the path component, serves to identify a resource within the scope of the URI's scheme and naming authority."

    query       = *( pchar 
                   | "/" 
                   | "?" )
"The fragment identifier component of a URI allows indirect identification of a secondary resource by reference to a primary resource and additional identifying information."

    fragment    = *( pchar 
                   | "/" 
                   | "?" )

    pchar       = unreserved | pct-encoded | sub-delims | ":" | "@"
    
    unreserved  = ALPHA | DIGIT | "-" | "." | "_" | "~"
    sub-delims  = "!" | "$" | "&" | "'" | "(" | ")" | "*" | "+" | "," | ";" | "="

#### _Path_
"The path component contains data, usually organized in hierarchical form, that, along with data in the non-hierarchical query component."
"The path is terminated by the first question mark ("?") or number sign ("#") character, or by the end of the URI."
Very generalized path format compared to RFC 3986's format. I considered a mix between path-abempty and path-rootless: the path can begin by "/" or a segment, and is then a succession of segments. 

    path    = segment *( "/"  segment)

    segment = *pchar

### What about Response

General structure

    Response            = Status-Line                
                          *(( general-header        
                            | response-header        
                            | entity-header ) CRLF)  
                          CRLF
                          [ message-body ]     

The status line contains the protocol version with numeric status code and textual phrase. 

    Status-Line         = HTTP-Version SP Status-Code SP Reason-Phrase CRLF

Status codes:
<ul>
<li>1xx: Informational</li>
<li>2xx: Success</li>
<li>3xx: Redirection, further action will be made</li>
<li>4xx: Client Error, bad syntax or error while processing the request</li>
<li>5xx: Server Error, request was valid but server failed</li>
