import { useEffect, useState } from "react";

const POST = {
  method: "POST",
  headers: { "Content-Type": "application/json" },
};

function InputSection() {
  const [name, setName] = useState("");
  const [greeting, setGreeting] = useState("");

  function handleClick() {
    fetch("http://localhost:5001/example/hello", {
      ...POST,
      body: JSON.stringify({ name }),
    })
      .then((response) => response.json())
      .then((json) => setGreeting(json.message))
      .catch();
  }

  return (
    <>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Name?"
      />
      <button onClick={handleClick}>Submit</button>
      <p>{greeting}</p>
    </>
  );
}

function App() {
  const [firstElem, setFirstElem] = useState();
  const [secondElem, setSecondElem] = useState();

  useEffect(() => {
    fetch("http://localhost:5001/example/12")
      .then((response) => response.json())
      .then((json) => {
        setFirstElem(json.firstElem);
        setSecondElem(json.secondElem);
      })
      .catch((_error) => {});
  }, []);

  return (
    <>
      <h1>Example of API</h1>
      <h2>GET example:</h2>
      <ul>
        <li>{firstElem}</li>
        <li>{secondElem}</li>
      </ul>
      <h2>POST example:</h2>
      <InputSection />
    </>
  );
}

export default App;
