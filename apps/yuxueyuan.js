var result = null;
function get_sign(body) {
  Java.perform(function () {
    try {
      var ksecurity = Java.use('com.drcuiyutao.lib.api.APIUtils');
      result = ksecurity.updateBodyString(body)
      console.log("myfunc result: " + result);
    } catch (e) {
      console.log(e)
    }
  });
  return result;
}


rpc.exports = {
  getSign: get_sign,
}