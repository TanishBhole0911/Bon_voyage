//write an api request to  http://127.0.0.1:8000
const data = {
  Place: "Lucknow",
  Food: "local",
  Interests: "Adventure, Religion",
  Health: "None",
  Days: 5,
  email: "abc@gmail.com",
  in_date: "06-04-2024",
  out_date: "06-04-2024",
};

fetch("http://127.0.0.1:8000/chat", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(data),
})
  .then((response) => response.json())
  .then((data) => {
    console.log("Success:", data);
  })
  .catch((error) => {
    console.error("Error:", error);
  });
