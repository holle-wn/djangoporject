const cookieUtil = require('../../utils/util.js')
const szStock = require('../../resources/data/stock/sz-100.js')
const shStock = require('../../resources/data/stock/sh-100.js')


var allStockData = []
Array.prototype.push.apply(allStockData, szStock.data)
Array.prototype.push.apply(allStockData, shStock.data)

const app = getApp()

Page({
  data: {
    isConstellPicker: false,
    isStockPicker: false,
    isCityPicker: false,

    personal: {
      constellation: [],
      city: [],
      stock: []
    },

    allPickerData: {
      allConstellation: ['白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座', '摩羯座', '水瓶座', '双鱼座'],
      allStock: allStockData
    }
  },

  onLoad: function(options) {
    this.setData({
      isConstellPicker: false,
      isStockPicker: false,
      isCityPicker: false
    })
    if (options.type == 'city'){
      this.setData({
        isCityPicker: true
      })
    }else if (options.type == 'constellation'){
      this.setData({
        isConstellPicker: true
      })
    }else if (options.type == 'stock'){
      this.setData({
        isStockPicker: true
      })
    }

    var header = {}
    var cookie = cookieUtil.getCookieFromStorage()
    header.Cookie = cookie
    var that = this
    wx.request({
      url: 'http://127.0.0.1:8000/juhe/v1.0/user',
      method: 'GET',
      header: header,
      success: function(res){
        console.log(res.data)
        that.setData({
          personal: res.data.focus
        })
        
      }
    })
  },

  // 保存后台
  onSave: function (isShowModal = true) {
    var header = {}
    var cookie = cookieUtil.getCookieFromStorage()
    header.Cookie = cookie
    var that = this
    wx.request({
      url: 'http://127.0.0.1:8000/juhe/v1.0/user',
      method: 'POST',
      data: {
        city: that.data.personal.city,
        stock: that.data.personal.stock,
        constellation: that.data.personal.constellation
      },
      header: header,
      success: function(res){
        console.log(res)
        wx.showModal({
          title: '保存成功',
          content: '',
        })
      }
    })
  },

  // 星座运势picker变更
  bindConstellationPickerChange: function(e) {
    console.log('constellPicker发送选择改变，携带值为', e.detail.value)
    var newItem = this.data.allPickerData.allConstellation[e.detail.value]
    var newData = this.data.personal.constellation
    // 去重
    if (newData.indexOf(newItem) > -1)
      return
    newData.push(newItem)
    var newPersonalData = this.data.personal
    newPersonalData.constellation = newData
    this.setData({
      personal: newPersonalData
    })
  },

  // 股票运势picker变更
  bindStockPickerChange: function(e) {
    var newItem = this.data.allPickerData.allStock[e.detail.value]
    var newData = this.data.personal.stock
    // 去重
    for (var i = 0; i < newData.length; i++) {
      if (newData[i].name == newItem.name && newData[i].code == newItem.code && newData[i].market == newItem.market) {
        console.log('already exists.')
        return
      }
    }
    newData.push(newItem)
    var newPersonalData = this.data.personal
    newPersonalData.stock = newData
    this.setData({
      personal: newPersonalData
    })
  },

  // 地区picker变更
  bindRegionPickerChange: function(e) {
    console.log('cityPicker发送选择改变，携带值为', e.detail.value)
    var pickerValue = e.detail.value
    var newItem = {
      province: pickerValue[0],
      city: pickerValue[1],
      area: pickerValue[2],
    }
    var newData = this.data.personal.city
    // 去重
    for (var i = 0; i < newData.length; i++) {
      if (newData[i].province == newItem.province && newData[i].city == newItem.city && newData[i].area == newItem.area) {
        console.log('already exists.')
        return
      }
    }
    newData.push(newItem)
    var newPersonalData = this.data.personal
    newPersonalData.city = newData
    this.setData({
      personal: newPersonalData
    })
  },

  // 删除列表元素
  deleteItem: function(e) {
    var that = this
    var deleteType = e.currentTarget.dataset.type
    var index = e.currentTarget.dataset.index
    console.log('delete type: ' + deleteType)
    console.log('delete index: ' + index)
    var personalData = this.data.personal
    wx.showModal({
      content: "确认删除此项吗？",
      showCancel: true,
      success: function(res) {
        console.log(res)
        if (res.confirm) {
          if (deleteType == 'constellation') {
            personalData.constellation.splice(index, 1)
          } else if (deleteType == 'stock') {
            personalData.stock.splice(index, 1)
          } else {
            personalData.city.splice(index, 1)
          }
          that.setData({
            personal: personalData
          })
          that.onSave(false)
        }
      }
    })
  }
});