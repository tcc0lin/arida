const babel = require('@babel/core')
var exports = new Map();
var functions = new Map();
var result = new Map();
function parse(code) {
  let visitor = {
    // 处理exports节点，获取导出函数对应表
    ExpressionStatement(path) {
      let params = path.node.expression.right;
      try {
        params = params.properties
        for (let i = 0; i < params.length; i++) {
          exports.set(params[i].value.name, params[i].key.name)
        }
      } catch {

      }
    },
    // 处理function，获取函数名以及对应参数
    FunctionDeclaration(path) {
      let params = path.node;
      functions.set(params.id.name, params.params.length)
    }
  }
  babel.transform(code, {
    plugins: [
      {
        visitor
      }
    ]
  })
  exports.forEach(function (value, key, map) {
    result.set(value, functions.get(key))
  })
  return Object.fromEntries(result);
}