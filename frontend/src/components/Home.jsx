import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import Result from "./Result";
import fetchSearch from "../hooks/fetchSearch";
const Home = () => {
  const [requestParams, setRequestParams] = useState({
    searchMode: "all",
    query: "",
  });
  const searchModes = ["all", "keyword", "semantic"];
  const {data, isFetching} = useQuery(["search", requestParams], fetchSearch);
  const products = data?.products ?? [];
  return (
    <div className="container">
      <form
        onSubmit={(e) => {
          e.preventDefault();
          const formData = new FormData(e.target);
          console.log(formData.get("query"))
          console.log(formData.get("mode"))
          setRequestParams({
            query: formData.get("query") ?? "",
            searchMode: formData.get("mode") ?? "",
          });
        }}
      >
        <div className="row">
          <div className="col-md-8">
          <input placeholder="Enter waht you want ..." id="query" name="query" className="form-control form-control-lg" />
          </div>
          <div className="col-md-2">
          <select
          id="mode"
          name="mode"
          className="form-control form-control-lg select"
        >
          {searchModes.map((a) => (
            <option key={a}>{a}</option>
          ))}
        </select>
          </div>
          <div className="col-md-2">
          <button className="btn btn-lg">Submit</button>

          </div>
          
        </div>
       
        
  
      </form>
      <Result products={products} isFetching={isFetching}/>
    </div>
    
  );
};

export default Home;
