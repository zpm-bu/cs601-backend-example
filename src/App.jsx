import { useEffect, useState } from "react";

function App() {
  const [firstElem, setFirstElem] = useState();
  const [secondElem, setSecondElem] = useState();

  useEffect(() => {
    fetch("http://localhost:5000/example/12")
      .then((response) => response.json())
      .then((json) => {
        setFirstElem(json.firstElem);
        setSecondElem(json.secondElem);
      })
      .catch((_error) => {});
  }, []);

  return (
    <>
      <ul>
        <li>{firstElem}</li>
        <li>{secondElem}</li>
      </ul>
    </>
  );
}

export default App;
