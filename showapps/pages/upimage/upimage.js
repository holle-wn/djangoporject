Page({
  data: {
    files: [],
    downloadedBackupedFiles: []
  },
  chooseImage: function(e) {
    var that = this;
    wx.chooseImage({
      sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
      success: function(res) {
        // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片
        that.setData({
          files: that.data.files.concat(res.tempFilePaths)
        });
      }
    })
  },
  previewImage: function(e) {
    wx.previewImage({
      current: e.currentTarget.id, // 当前显示图片的http链接
      urls: this.data.files // 需要预览的图片http链接列表
    })
  },
  upload:function(){
    for( var i=0; i<this.data.files.length; i++){
      var filepath = this.data.files[i]
      wx.uploadFile({
        url: 'http://127.0.0.1:8000/juhe/v1.0/image1',
        filePath: filepath,
        name: filepath,
        success:function(res){
          console.log(res.data)
        }
      })
    }; 
  },
  loadpic: function(imgItem){
    var that = this
    wx.downloadFile({
      url: 'http://127.0.0.1:8000/juhe/v1.0/image1',
      success:function(res){
        console.log('成功了...')
        var tmpPath =res.tempFilePath
        var newDownloadeDackupedFiles = that.data.downloadedBackupedFiles
        newDownloadeDackupedFiles.push(tmpPath)
        that.setData({
          downloadedBackupedFiles: newDownloadeDackupedFiles
        })
      }
    })
  },
  deletepic: function(){
    wx.request({
      url: 'http://127.0.0.1:8000/juhe/v1.0/image1?name=b.jpg',
      method:'DELETE',
      success: function(res){
        console.log(res.data)
        wx.showToast({
          title: '删除成功',
        })
      }
    })
  },
  longTapConfirm: function(e){
    var that = this
    var confirmList = ['删除这个图片']
    wx.showActionSheet({
      itemList: confirmList,
      success: function(res){
        var imageIndex = e.currentTarget.dataset.index
        var imageItem = that.data.downloadedBackupedFiles[imageIndex]
        var newlist = that.data.downloadedBackupedFiles
        newlist.splice(imageIndex, 1)
        that.setData({
          downloadedBackupedFiles: newlist
        })
      }
    })
  }
});