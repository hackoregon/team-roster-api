# Team Roster API

This API uses a Google Sheet as a backend to power a Lambda API for the Hack Oregon team roster.

## API Function

The API function reads Google credentials from the AWS Parameter Store in order to read the team roster from a Google Sheet using the `gsheets` package.

## Resizer Function

The Resizer function runs every time a new image is added to the `hacko-profiles-original`. It resizes the image and uploads it to the same path in the `hacko-profiles-resized` bucket.

## Adding images

The easiest way to add images to the `hacko-profiles-original` bucket is to use the AWS CLI.

```
aws s3 cp --recursive . s3://hacko-profiles-original
```

## Deploying

Deploying these functions is more complicated than you might expect because they rely on packages that need to be bundled and uploaded along with the Python source. Further more, the resizer function requires PIL, which needs to be built for the architecture of underlying server (so much for serverless, amirite?).

It's all captured in a Makefile though.

`make vendor`: This will create a local `vendor` directory that includes all the requisite packages to be uploaded, including the Linux `PIL` precompiled via a `.whl` file.

`make package`: This will create zip files for each function by zipping the `vendor` dir and adding the source function to each bundle.

`make publish`: This will update the source code for the two Lambda functions.
