## Machine Learning University: Bedrock Agents

This repository contains a couple of notebooks for the __Bedrock Agents__ class at  __Amazon Machine Learning University__ . Our mission is to make Machine Learning accessible to everyone. We have courses available across many topics of machine learning and believe knowledge of ML can be a key enabler for success. These notebook represent some real-world use cases with Bedrock Agents.

---

__Project : Application Builder Assistant using Bedrock Agents and multiple knowledge bases__

| Title | Studio lab |
| :---: | ---: |
| Application Builder Assistant using Bedrock Agents| ai_appbuilder_assistant/BedrockAgents_AI_AppBuilder_Assistant.ipynb|

---

__Setup Instructions__

Download the knowledge base files as per `readMe.txt` instructions in both of these locations

 1. `kb_appbuilder/aws_best_practices_2/readMe.txt`
 2. `kb_appbuilder/northwind_db/readMe.txt`

---
__Troubleshooting: CFN template__

Please add the following independent role in `SageMaker_Bedrock_Agents.yaml` if you get the following error:

`SageMaker is not authorized to perform: iam:CreateServiceLinkedRole on resource: arn:aws:iam::<account-id>:role/aws-service-role/observability.aoss.amazonaws.com/AWSServiceRoleForAmazonOpenSearchServerless because no identity-based policy allows the iam:CreateServiceLinkedRole action`


```
AOSSLinkedRole:
    Type: AWS::IAM::ServiceLinkedRole
    Properties:
      AWSServiceName: observability.aoss.amazonaws.com
```

---

## License

The license for this repository depends on the section.  Data set for the course is being provided to you by permission of Amazon and is subject to the terms of the [Amazon License and Access](https://www.amazon.com/gp/help/customer/display.html?nodeId=201909000). You are expressly prohibited from copying, modifying, selling, exporting or using this data set in any way other than for the purpose of completing this course. The lecture slides are released under the CC-BY-SA-4.0 License.  This project is licensed under the Apache-2.0 License. See each section's LICENSE file for details.
