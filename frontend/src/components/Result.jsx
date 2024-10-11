import Product from "./Product";

const Result = ({ products, isFetching}) => {
  const rows = []
  for (let i = 0; i < products.length; i += 4) {
    rows.push(products.slice(i, i + 4));
  }
  const msg = isFetching ? "Fetching Data ..." : "No Products Found!"

  return (
    <div>
      {!products.length ? (
        <h3 id="loading-msg">{msg}</h3>
      ) : (
        <div className="data">
          {rows.map((row, rowIndex) => (
            <div className="row" key={`row-${rowIndex}`}>
              {row.map((product) => (
                <div className="col-md-3 col-xs-12" key={product.id}>
                  <Product {...product} />
                </div>
              ))}
            </div>
          ))}
    </div>
      )}
    </div>
  );
};
export default Result;
