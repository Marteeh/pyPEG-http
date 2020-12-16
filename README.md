# pyPEG-http
A pyPEG parser for HTTP request/response

**1st step**: Getting used to pyPEG with simple HTTP requests (GET)

## Full Grammar - following RFC 2616:

### Basic structure

    generic-message =   start-line
                        *(message-header CRLF)
                        CRLF
                        [ message-body ]
    start-line      =   Request-Line | Status-Line
    message-header  =   field-name ":" [ field-value ]
    field-name      =   token
    field-content   =   the OCTETs making up the field-value and consisting of either *TEXT or combinations of token, separators, and quoted-string

### Getting into Request

The request defines the action to be applied to a specified ressource, its identifier and used protocol

    Request             = Request-Line              
                          *((   general-header        
                            | request-header         
                            | entity-header ) CRLF) 
                          CRLF
                          [ message-body ]

SP character = space which has to be indicated to pyPEG.

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

"The four options for Request-URI are dependent on the nature of the request."

    Request-URI         =   "*" | absoluteURI | abs_path | authority

### What about Response

General structure

    Response            = Status-Line                
                          *((   general-header        
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
