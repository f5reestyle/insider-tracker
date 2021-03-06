import React, { useState } from "react";
import Axios from "axios";
import {
  Card,
  Form,
  Input,
  Button,
  Checkbox,
  notification,
  Row,
  Col,
} from "antd";
import { SmileOutlined } from "@ant-design/icons";
import { useHistory } from "react-router-dom";

const layout = {
  labelCol: { span: 8 },
  wrapperCol: { span: 16 },
};
const tailLayout = {
  wrapperCol: { offset: 8, span: 16 },
};

export default function Signup() {
  const history = useHistory();
  const [fieldErrors, setFieldErrors] = useState({});
  const [email, setEmail] = useState("");
  const [api_key, setApi_key] = useState("");
  const [loading, setLoading] = useState(false);

  async function onClick(e) {
    e.preventDefault();
    try {
      setLoading(true);
      console.log({ email });
      const response = await Axios.post(
        "http://localhost:8000/accounts/email/",
        { email }
      );
      setFieldErrors((prev) => ({
        ...prev,
        email: {
          hasFeedback: true,
          validateStatus: "success",
          help: "API key is successfully issued!",
        },
      }));
      console.log(fieldErrors);
      setLoading(false);
      setApi_key(response.data.api_key);
    } catch (error) {
      console.log(error);
      setLoading(false);
    }
  }
  async function onFinish(values) {
    const { username, password } = values;
    const data = { username, password, email, api_key };
    try {
      const response = await Axios.post(
        "http://localhost:8000/accounts/signup/",
        data
      );
      notification.open({
        message: "회원가입에 성공하였습니다.",
        description: "로그인 페이지로 이동합니다.",
        icon: <SmileOutlined style={{ color: "#108ee9" }} />,
      });
      history.push("/accounts/login");
    } catch (error) {
      if (error.response) {
        const { data: fieldsErrorMessages } = error.response;
        // fieldsErrorMessages => { username : ["m1","m2"], password : [] } 꼴임
        // 필드의 에러메세지 리스트 원소들 하나의 문자열로 합치기
        console.log(fieldsErrorMessages);
        setFieldErrors(
          Object.entries(fieldsErrorMessages).reduce((acc, [field, errors]) => {
            acc[field] = {
              validateStatus: "error",
              help: errors.join(" "),
            };
            return acc;
          }, {})
        );
      }
    }
  }
  return (
    <Card title="Signup">
      {api_key}
      <Form
        {...layout}
        name="basic"
        initialValues={{ remember: true }}
        onFinish={onFinish}
      >
        <Form.Item
          label="Username"
          name="username"
          rules={[
            { required: true, message: "Please input your username!" },
            { min: 5, message: "5글자 이상 플리즈" },
          ]}
          hasFeedback
          {...fieldErrors.username}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Password"
          name="password"
          rules={[{ required: true, message: "Please input your password!" }]}
          hasFeedback
          {...fieldErrors.password}
        >
          <Input.Password />
        </Form.Item>
        <Form.Item label="email">
          <Row gutter={8}>
            <Col span={16}>
              <Form.Item
                name="email"
                rules={[
                  {
                    required: true,
                    message: "Please input your email!",
                  },
                ]}
                {...fieldErrors.email}
              >
                <Input onChange={(e) => setEmail(e.target.value)} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Button loading={loading} onClick={onClick}>
                get API Key!
              </Button>
            </Col>
          </Row>
        </Form.Item>

        <Form.Item {...tailLayout}>
          <Button type="primary" htmlType="submit">
            Submit
          </Button>
        </Form.Item>
      </Form>
    </Card>
  );
}
