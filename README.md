# pyPEG-http
A pyPEG parser for HTTP request/response

**1st step**: Getting used to pyPEG with simple HTTP requests (GET)

## Full Grammar -thanks to RFC 2616:
Basic structure

> generic-message =   start-line
>                     *(message-header CRLF)
>                     CRLF
>                     [ message-body ]
> start-line      =   Request-Line | Status-Line
> message-header  =   field-name ":" [ field-value ]
> field-name      =   token
> field-content   =   the OCTETs making up the field-value
>                     and consisting of either *TEXT or combinations
>                     of token, separators, and quoted-string

Getting into Request
"The four options for Request-URI are dependent on the nature of the request."

> Request           =   Request-Line              
>                       *(  ( general-header        
>                           | request-header         
>                           | entity-header ) CRLF) 
>                       CRLF
>                       [ message-body ]
> Request-Line      =   Method SP Request-URI SP HTTP-Version CRLF
> Method            =   "OPTIONS"                
>                   |   "GET"                    
>                   |   "HEAD"                   
>                   |   "POST"                   
>                   |   "PUT"                    
>                   |   "DELETE"                                      
>                   |   "TRACE"                  
>                   |   "CONNECT"                
>                   |   extension-method
> Request-URI       =   "*" | absoluteURI | abs_path | authority