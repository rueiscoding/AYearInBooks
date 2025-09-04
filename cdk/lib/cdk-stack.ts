import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as iam from 'aws-cdk-lib/aws-iam';

export class GoodreadsWrappedStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    //s3 for csv uploads
    const csvBucket = new s3.Bucket(this, 'GoodreadsWrappedBucket', {
      versioned: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
        cors: [
        {
          allowedOrigins: ['http://localhost:5173'],
          allowedMethods: [
            s3.HttpMethods.PUT,
            s3.HttpMethods.GET,
            s3.HttpMethods.POST,
          ],
          allowedHeaders: ['*'], // any headers
          maxAge: 3000,
        },
      ],
    });

    // lambda function for uploading csv
    const getUploadUrlFn = new lambda.Function(this, 'GetUploadUrlFn', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'index.handler',
      code: lambda.Code.fromAsset('lambda/get-upload-url'),
      environment: {
        CSV_BUCKET: csvBucket.bucketName,
      },
    });


    // api gateway
    const api = new apigateway.RestApi(this, 'GoodreadsWrappedApi', {
      restApiName: 'GoodreadsWrapped Service',
      description: 'Serverless API for Goodreads Wrapped',
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS,
        allowMethods: apigateway.Cors.ALL_METHODS,
      },
    });


    const uploadResource = api.root.addResource('get-upload-url');
    uploadResource.addMethod(
      'GET',
      new apigateway.LambdaIntegration(getUploadUrlFn),
      {
        authorizationType: apigateway.AuthorizationType.NONE,
      },
    );


    new cdk.CfnOutput(this, 'ApiEndpoint', {
      value: api.url ?? 'Something went wrong',
    });
  }
}
