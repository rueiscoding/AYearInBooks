import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import crypto from "crypto";

const s3 = new S3Client({
  region: process.env.AWS_REGION || "us-east-1"
});

export const handler = async (event) => {


  console.log("Event:", JSON.stringify(event, null, 2));

  if (event.httpMethod === "OPTIONS") {
    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,GET,PUT,POST",
        "Access-Control-Allow-Headers": "Content-Type",
      },
      body: "",
    };
  }

  try {

    const key = `${crypto.randomUUID()}.csv`;

    const command = new PutObjectCommand({
      Bucket: process.env.CSV_BUCKET,
      Key: key,
      ContentType: "text/csv",
    });

    const uploadUrl = await getSignedUrl(s3, command, { expiresIn: 60 });

    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,GET,PUT,POST",
        "Access-Control-Allow-Headers": "Content-Type",
      },
      body: JSON.stringify({ uploadUrl, key }),
    };

  } catch (error) {
    console.error("Error:", error);

    return {
      statusCode: 500,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,GET,PUT,POST",
        "Access-Control-Allow-Headers": "Content-Type",
      },
      body: JSON.stringify({
        error: "Internal server error",
        message: error.message,
      }),
    };
  }
};
