import React from "react";
import ReactDOM from "react-dom";
import TestProvider from "tests/TestProvider";
import HeaderButtons from "./HeaderButtons";

it("renders without crashing", () => {
  const div = document.createElement("div");
  ReactDOM.render(
    <TestProvider>
      <HeaderButtons />
    </TestProvider>,
    div
  );
  ReactDOM.unmountComponentAtNode(div);
});
