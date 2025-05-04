const express = require("express");
const nunjucks = require("nunjucks");

const app = express();
nunjucks.configure("views", {
  autoescape: true,
  express: app,
});

app.get("/", function (req, res) {
  const input = req.query.value || "";
  if (!input) {
    return res.render("index.html", { message: "Please provide an input" });
  }
  if (input.includes(" ")) {
    return res.render("index.html", { message: "Sorry, we only accept space-free palindromes here!" });
  }
  const reversed = [...input].reverse().join("");
  let message = "";
  if (input && input === reversed) {
    message = nunjucks.renderString((str = reversed + " is a very nice palindrome"));
  } else if (input) {
    message = nunjucks.renderString((str = "You string reversed is not a palindrome: " + reversed));
  }
  
  return res.render("index.html", { message: message });
});

const server = app.listen(process.env.PORT || 80, () => {
  console.log(`Server started on port: ${server.address().port}`);
});
