function trim(text) {
    return text.replace(/^\s+/, "").replace(/\s+$/, "");
}

function checkPhonenum(phonenum) {
    var p = phonenum.toString();
    return true;
}

function checkEmail(email) {
    var myreg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
    return myreg.test(email);
}

function checkdinfo() {
    for (var i = 0; i < 32; i++) {
        if (i != 14) document.form1.elements[i].value = trim(document.form1.elements[i].value);
    }
    if ("" == document.getElementById('email').value) {
        alert("请填写您的电子邮箱");
        document.getElementById('email').focus();
        return false;
    } else if ("" == document.getElementById('qqnum').value) {
        alert("请填写您的QQ号");
        document.getElementById('qqnum').focus();
        return false;
    } else if ("" == document.getElementById('classid').value) {
        alert("请填写您的班级");
        document.getElementById('classid').focus();
        return false;
    } else if ("" == document.form1.elements[26].value) {
        alert("请填写您的监护人信息");
        document.form1.elements[26].focus();
        return false;
    } else if ("" == document.form1.elements[27].value) {
        alert("请填写您的监护人信息");
        document.form1.elements[27].focus();
        return false;
    } else if ("" == document.form1.elements[28].value) {
        alert("请填写您的监护人信息");
        document.form1.elements[28].focus();
        return false;
    } else if ("" == document.form1.elements[29].value) {
        alert("请填写您的监护人信息");
        document.form1.elements[29].focus();
        return false;
    } else if ("" == document.form1.elements[31].value) {
        alert("请填写您的监护人信息");
        document.form1.elements[31].focus();
        return false;
    } else if (!checkEmail(document.getElementById('email').value)) {
        alert("请检查您填写的电子邮箱");
        document.getElementById('email').focus();
        return false;
    } else if (!checkPhonenum(document.form1.elements[31].value)) {
        alert("请检查您填写的监护人电话");
        document.form1.elements[31].focus();
        return false;
    } else if (document.form1.elements[14].files.length <= 0) {
        alert("请上传您的照片");
        document.form1.elements[14].focus();
        return false;
    } else if (document.form1.elements[14].files[0].size > (1024 * 1024)) {
        alert("您上传的照片过大");
        document.form1.elements[14].focus();
        return false;
    }

    var name = document.form1.elements[14].value;
    var fileType= name.substring(name.lastIndexOf(".")+1).toLowerCase();
    if(fileType != "jpg" && fileType != "jpeg" && fileType != "png") {
        alert("文件格式不对！");
        document.form1.elements[14].value = "";
        return false;
    }

    return true;
}
