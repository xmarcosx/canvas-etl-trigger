# canvas-cloud-function

Test locally:
```bash
cd src;
functions-framework --target=canvas;
```

http://localhost:8080/?endpoint=terms&start_date=2020-08-01

Deploy function:

```bash
cd src;
gcloud functions deploy canvas \
--runtime python37 \
--trigger-http;
```
