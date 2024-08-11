"use client";
import { builder, Builder, withChildren } from "@builder.io/react";
import BusinessRegistrationForm from "./components/RegisterBusiness/BusinessRegistrationForm";
import Button from "./components/Button";
import Button from "./components/registration/Button";
import CallToAction from "./components/CallToAction";
import ContentSection from "./components/ContentSection";
import Counter from "./components/Counter/Counter";
import Footer from "./components/Footer";
import FormInput from "./components/FormInput";
import FormInput from "./components/registration/FormInput";
import Header from "./components/Header";
import Layout from "./components/Layout";
import MyComponent from "./components/MyComponent";
import RegisterBusinessPage from "./components/RegisterBusiness/RegisterBusinessPage";
import RegistrationForm from "./components/RegistrationForm";
import RegistrationForm from "./components/registration/RegistrationForm";
import RegistrationPage from "./components/registration/RegistrationPage";
import SubmitButton from "./components/RegisterBusiness/SubmitButton";

builder.init(process.env.NEXT_PUBLIC_BUILDER_API_KEY!);

Builder.registerComponent(Counter, {
  name: "Counter",
  inputs: [
    {
      name: "initialCount",
      type: "number",
    },
  ],
});

Builder.registerComponent(CallToAction, {
  name: "CallToAction",
});

Builder.registerComponent(ContentSection, {
  name: "ContentSection",
  inputs: [
    {
      name: "imageUrl",
      type: "string",
      required: true,
    },
    {
      name: "isReversed",
      type: "boolean",
    },
    {
      name: "text",
      type: "string",
      required: true,
    },
  ],
});

Builder.registerComponent(Footer, {
  name: "Footer",
});

Builder.registerComponent(Header, {
  name: "Header",
});

Builder.registerComponent(withChildren(Layout), {
  name: "Layout",
  inputs: [
    {
      name: "children",
      type: "string",
      hideFromUI: true,
      meta: {
        ts: "ReactNode",
      },
    },
  ],
});

Builder.registerComponent(MyComponent, {
  name: "MyComponent",
});

Builder.registerComponent(withChildren(Button), {
  name: "Button",
  inputs: [
    {
      name: "children",
      type: "string",
      hideFromUI: true,
      meta: {
        ts: "ReactNode",
      },
    },
    {
      name: "className",
      type: "string",
    },
  ],
});

Builder.registerComponent(FormInput, {
  name: "FormInput",
  inputs: [
    {
      name: "label",
      type: "string",
      required: true,
    },
    {
      name: "placeholder",
      type: "string",
      required: true,
    },
  ],
});

Builder.registerComponent(RegistrationForm, {
  name: "RegistrationForm",
});

Builder.registerComponent(withChildren(Button), {
  name: "Button",
  inputs: [
    {
      name: "children",
      type: "string",
      hideFromUI: true,
      meta: {
        ts: "ReactNode",
      },
    },
    {
      name: "className",
      type: "string",
    },
  ],
});

Builder.registerComponent(FormInput, {
  name: "FormInput",
  inputs: [
    {
      name: "label",
      type: "string",
      required: true,
    },
    {
      name: "placeholder",
      type: "string",
      required: true,
    },
    {
      name: "type",
      type: "string",
    },
  ],
});

Builder.registerComponent(withChildren(Button), {
  name: "Button",
  inputs: [
    {
      name: "children",
      type: "string",
      hideFromUI: true,
      meta: {
        ts: "ReactNode",
      },
    },
    {
      name: "className",
      type: "string",
    },
  ],
});

Builder.registerComponent(FormInput, {
  name: "FormInput",
  inputs: [
    {
      name: "label",
      type: "string",
      required: true,
    },
    {
      name: "placeholder",
      type: "string",
      required: true,
    },
    {
      name: "type",
      type: "string",
    },
  ],
});

Builder.registerComponent(RegistrationPage, {
  name: "RegistrationPage",
});

Builder.registerComponent(RegistrationForm, {
  name: "RegistrationForm",
});

Builder.registerComponent(withChildren(Button), {
  name: "Button",
  inputs: [
    {
      name: "children",
      type: "string",
      hideFromUI: true,
      meta: {
        ts: "ReactNode",
      },
    },
    {
      name: "className",
      type: "string",
    },
  ],
});

Builder.registerComponent(BusinessRegistrationForm, {
  name: "BusinessRegistrationForm",
});

Builder.registerComponent(withChildren(Button), {
  name: "Button",
  inputs: [
    {
      name: "children",
      type: "string",
      hideFromUI: true,
      meta: {
        ts: "ReactNode",
      },
    },
    {
      name: "className",
      type: "string",
    },
  ],
});

Builder.registerComponent(RegisterBusinessPage, {
  name: "RegisterBusinessPage",
});

Builder.registerComponent(RegistrationForm, {
  name: "RegistrationForm",
});

Builder.registerComponent(FormInput, {
  name: "FormInput",
  inputs: [
    {
      name: "label",
      type: "string",
      required: true,
    },
    {
      name: "placeholder",
      type: "string",
      required: true,
    },
    {
      name: "type",
      type: "string",
    },
  ],
});

Builder.registerComponent(RegistrationForm, {
  name: "RegistrationForm",
});

Builder.registerComponent(SubmitButton, {
  name: "SubmitButton",
  inputs: [
    {
      name: "text",
      type: "string",
      required: true,
    },
  ],
});
