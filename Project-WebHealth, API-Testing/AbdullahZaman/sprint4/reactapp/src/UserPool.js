import { CognitoUserPool } from "amazon-cognito-identity-js";

const poolData = {
    UserPoolId : "us-east-2_4jLoR9IFm",
    ClientId : "2aqrqav19cs41952c1l4ub58bb"
}

export default new CognitoUserPool(poolData);