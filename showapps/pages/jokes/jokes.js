// pages/jokes/jokes.js
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  onLoad: function() {
    var that = this
    var timestamp = Date.parse(new Date());
    wx.request({
      url: 'http://v.juhe.cn/joke/content/list.php?sort=desc & page=1& pagesize=5& time=' + timestamp / 1000 + '& key=89cd369a91f356e8a134468632739979',
      success: function(res) {
        console.log(res.data.result.data)
        that.setData({
          content: res.data.result.data
        })
      }
    })

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function() {

  }
})