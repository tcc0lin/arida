var result = null;
function decrypt_data(data) {
  Java.perform(function () {
    var rc_class = Java.use("com.baidu.android.common.security.RC4");
    var func_class = Java.use("com.kuaiduizuoye.scan.utils.a.a");
    var func_instance = func_class.$new();
    var stringClass = Java.use("java.lang.String");
    var stringInstance = stringClass.$new("4edb41c838d8a5c38b772854523658ea6a5f03f2d598caf9f8062e2d5f8d0ed16cc5f1e130de80b44a740cf8e01fdfc931cd22941af1d9898bc5ba70303e73a5");
    var rc = rc_class.$new(stringInstance);
    result = func_instance.a(data, rc, false);
  });
  return result;
}
function generate_url(origin_url) {
  Java.perform(function () {
    var search_common_api = Java.use("com.kuaiduizuoye.scan.common.net.model.v1.SearchCommonApi$Input");
    var input_base = search_common_api.$new(origin_url);
    var func_class = Java.use("com.baidu.homework.common.net.Net");
    result = func_class.appendSign(input_base);
  });
  return result;
}
function encrypt_data(grade, subject, versionId, term, text, isHitDayup, bookType, isHitPay, dataType, pn, rn) {
  Java.perform(function () {
    var func_class = Java.use("com.kuaiduizuoye.scan.base.f");
    var search_search_api = Java.use("com.kuaiduizuoye.scan.common.net.model.v1.SearchSearch$Input");
    var input_base = search_search_api.$new(grade, subject, versionId, term, text, isHitDayup, bookType, isHitPay, dataType, pn, rn);
    result = func_class.a(input_base);
  });
  return result;
}
rpc.exports = {
  decryptData: decrypt_data,
  generateUrl: generate_url,
  encryptData: encrypt_data
}