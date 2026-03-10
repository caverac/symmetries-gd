import * as cdk from 'aws-cdk-lib'
import * as s3 from 'aws-cdk-lib/aws-s3'
import { Construct } from 'constructs'
import { DeploymentEnvironment } from 'utils/types'

export interface StorageStackProps extends cdk.StackProps {
  deploymentEnvironment: DeploymentEnvironment
}

export class StorageStack extends cdk.Stack {
  public readonly bucket: s3.Bucket

  constructor(scope: Construct, id: string, props: StorageStackProps) {
    super(scope, id, props)

    const isProd = props.deploymentEnvironment === 'production'

    this.bucket = new s3.Bucket(this, 'StorageBucket', {
      bucketName: `symmetries-gd-${props.deploymentEnvironment}`,
      blockPublicAccess: new s3.BlockPublicAccess({
        blockPublicAcls: false,
        ignorePublicAcls: false,
        blockPublicPolicy: false,
        restrictPublicBuckets: false
      }),
      objectOwnership: s3.ObjectOwnership.BUCKET_OWNER_PREFERRED,
      encryption: s3.BucketEncryption.S3_MANAGED,
      versioned: false,
      removalPolicy: isProd ? cdk.RemovalPolicy.RETAIN : cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: !isProd
    })

    this.bucket.grantPublicAccess('*', 's3:GetObject')
  }
}
