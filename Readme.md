S3 Cache
---
A simple download script that caches the most recently accessed files stored on Amazon S3 to save bandwidth. 

Quickstart
---

	docker run -p 8000:80 -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY -e S3_BUCKET=$S3_BUCKET -t bluelaguna/s3cache

Where $AWS_ACCESS_KEY_ID, $AWS_SECRET_ACCESS_KEY, and $S3_BUCKET are stored in environment variables or replaced with their actual values.

You should then be able to access a file stored in $S3_BUCKET using http://localhost:8000/download/path/to/file. This will redirect to Amazon S3 the first time, but send the file directly the second time.

More Info
---
More details about what's going on here can be found at my blog post at http://akeem.mclennon.com/2014/07/saving-bandwidth-on-amazon-s3-by-caching-the-most-recent-files/