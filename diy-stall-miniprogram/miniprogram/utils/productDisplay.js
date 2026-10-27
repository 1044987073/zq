/** 用户端展示用：库存文案、是否售罄 */
function decorateProduct(product) {
  const p = { ...product };
  const stock = p.stock;
  let stockLabel = '';
  if (stock === 0) stockLabel = '售罄';
  else if (stock != null && stock !== '' && !Number.isNaN(Number(stock))) {
    stockLabel = `剩余 ${stock}`;
  }
  return {
    ...p,
    stockLabel,
    soldOut: stock === 0
  };
}

function decorateList(list) {
  return (list || []).map(decorateProduct);
}

module.exports = { decorateProduct, decorateList };
