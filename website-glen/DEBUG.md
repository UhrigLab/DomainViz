## FAQ/Debugging

### Q: Why is the website returning a 502 Error when I run it, even with the example files?
#### A: This may be due to the API service being disabled/shut down. Enter the server's backend, run the command: `sudo systemctl status prodoplot` and check the results. The service should be Active. If it is Inactive/Dead, then restart it with `sudo systemctl restart prodoplot`
NOTE: The error we saw on the front end was `Oh dear. Something has gone wrong. The following error has occured: Error: Request failed with status code 502` and in the server logs (`access.log` and `error.log`) the error seen was:

`*252 connect() failed (111: Connection refused) while connecting to upstream, client: 142.***.***.215, server:, request: "GET /api/testFasta HTTP/1.1", upstream: "http://127.0.0.1:5000.api/testFasta", host "https://uhrigprotools.biology.ualberta.ca/domainviz"`

And this is how we knew that the API service was down.

### Q: Why is the website itself down?
#### A: This may be due to the FrontEnd service `nginx` being shut down, as above. Try fixing this with `sudo systemctl status nginx`, and restart the service if it is down.