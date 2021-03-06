import React, { useState } from "react";
import Axios from "axios";

import { storeWebAndContext } from "context/authentication/actions";
import { useHistory } from "react-router-dom";
import { useAuthContext } from "context/authentication/store";

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

const layout = {
  labelCol: { span: 8 },
  wrapperCol: { span: 16 },
};
const tailLayout = {
  wrapperCol: { offset: 8, span: 16 },
};

export default function Login({ location }) {
  const history = useHistory();
  const { store, dispatch } = useAuthContext();
  const [fieldErrors, setFieldErrors] = useState({});

  const {
    from: { pathname },
  } = location.state || { from: { pathname: "/" } };
  console.log("ggg", pathname);
  async function onFinish(values) {
    const { username, password } = values;
    const data = { username, password };
    try {
      const response = await Axios.post(
        "http://localhost:8000/accounts/token/",
        data
      );
      const { token, api_key } = response.data;
      
      storeWebAndContext(dispatch, token, api_key);

      notification.open({
        message: "로그인에 성공하였습니다.",
        description: "반갑습니다!",
        icon: <SmileOutlined style={{ color: "#108ee9" }} />,
      });
      history.push(pathname);
    } catch (error) {
      if (error.response) {
        const { data } = error.response;

        notification.error({
          message: "로그인에 실패하였습니다.",
          description: Object.values(data).join(" "),
        });
      }
    }
  }
  return (
    <Card title="Login">
      <Form
        {...layout}
        name="basic"
        initialValues={{ remember: true }}
        onFinish={onFinish}
      >
        <Form.Item
          label="Username"
          name="username"
          rules={[{ required: true, message: "Please input your username!" }]}
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

        <Form.Item {...tailLayout}>
          <Button type="primary" htmlType="submit">
            Submit
          </Button>
        </Form.Item>
      </Form>
    </Card>
  );
}
