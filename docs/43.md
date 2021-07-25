### AWS的其他服务

#### 资料
1. [通俗解释 AWS 50个云服务每个组件的作用](https://www.infoq.cn/article/HVzTm_rLLvgK1Dyqqb2B)

#### Device Farm（编程使用云设备、Device Farm）
```python
# test_demo.py
# 运行：pytest -s
import boto3, pytest
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import Remote

class TestDemo:
    def setup_method(self, method):
        devicefarm_client = boto3.client("devicefarm", region_name="us-west-2")
        testgrid_url_response = devicefarm_client.create_test_grid_url(
            projectArn="arn:aws:devicefarm:us-west-2:223422645499:testgrid-project:0a72e439-4fa2-48d4-9950-83764338e1e8",
            expiresInSeconds=300)
        self. driver = Remote(testgrid_url_response["url"], DesiredCapabilities.FIREFOX)
    def test_passing(self):
        assert (1, 2, 3) == (1, 2, 3)
    def teardown_method(self, method):
        self.driver.quit()
```

#### AppStream（类似Citrix）
1. Windows 远程桌面，按小时付费
1. 1核Windows每小时 0.075 USD，空闲时 0.019 USD
1. 用浏览器或者AppStream客户端访问

#### Workspaces
1. Windows、Linux 远程桌面，按月/小时付费
1. 1核Windows每小时 0.22 USD
1. 用浏览器或者Workspaces客户端访问

#### WorkDocs
1. 企业服务，类似DropBox

#### Service Catalog
1. 企业服务，用户可以访问你构建的预设应用目录     

#### XRay
1. Lambda 启动XRay：
  1. Console界面-Lambda-配置，启动启动XRay
  2. python语言需要定制的layer层：https://github.com/awsdocs/aws-lambda-developer-guide/tree/main/sample-apps/blank-python
  3. 默认ApiGateway没有集成XRay，需要在Console界面启动XRay（需要是REST Api）

#### Single Sign-On（SSO）
1. 启用AWS全球的SSO作为身份提供商，把AWS中国作为应用，见[教程](https://saml-doc.okta.com/SAML_Docs/How-to-Configure-SAML-2.0-for-Amazon-AppStream-2-0.html)
  1. AWS全球的SSO控制台添加应用，下载SAML文件
  2. AWS中国的IAM控制台添加身份提供商（需要步骤1的SAML文件）和登录角色，下载SAML：https://signin.amazonaws.cn/static/saml-metadata.xml
  3. AWS全球的SSO控制台编辑应用，上传步骤2的SAML文件
  4. AWS全球的SSO控制台编辑应用，Role栏类型是uri，值是步骤2的提供商和登录角色的arn，用逗号隔开；RoleSessionName栏是{user:email}
1. 上例是本地的Identity Store支持SAML的/OpenID场景，如果不支持，则需要一个Identity Broker，它的作用是：
  1. 请求本地的Identity Store，验证登录
  1. 请求AWS的STS获取temporary security credentials
  1. Client 使用temporary security credentials使用cli操作或者在console操作

#### Step Functions（替代SWF）

#### CloudFormation

#### OpsWorks
1. 批量服务器配置、部署和管理。
1. OpsWorks 是一款配置管理服务，提供 Chef 和 Puppet 的托管实例。Chef 和 Puppet 是自动化平台。

#### MediaConvert（原名 Elastic Transcoder）
1. 视频转码

#### VPC 相关
1. PrivateLink
2. Egress Internet Gateway
3. VPC peering
