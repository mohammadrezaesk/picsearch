const Product = ({ name, description, colors, current_price, images, id, currency, brand_name, link }) => {
  var hero = "http://pets-images.dev-apis.com/pets/none.jpg";
  brand_name = brand_name ? brand_name.toUpperCase() : "UNKNOWN"
  if (images.length) {
    hero = images[0];
  }
  return (
      <div className="wsk-cp-product">
        <div className="wsk-cp-img">
          <img src={hero} alt="Product" className="img-responsive" />
        </div>
        <div className="wsk-cp-text">
          <div className="category">
            <span>{brand_name}</span>
          </div>
          <div className="title-product">
            <h3>{name}</h3>
          </div>
          <div className="description-prod">
            <p>{description}</p>
          </div>
          <div className="card-footer">
            <div className="wcf-left"><span className="price">{currency} {current_price}</span></div>
            <div className="wcf-right"><a href={link} className="buy-btn">VISIT SHOP<i className="zmdi zmdi-shopping-basket"></i></a></div>
          </div>
        </div>
      </div>
  );
};

export default Product;
