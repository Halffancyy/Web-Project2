$.fn.imagesLoaded = function (callback) {
  var elems = this.find("img"),
    elems_src = [],
    self = this,
    len = elems.length;
  if (!elems.length) {
    callback.call(this);
    return this;
  }
  elems
    .one("load error", function () {
      if (--len === 0) {
        len = elems.length;
        elems
          .one("load error", function () {
            if (--len === 0) {
              callback.call(self);
            }
          })
          .each(function () {
            this.src = elems_src.shift();
          });
      }
    })
    .each(function () {
      elems_src.push(this.src);
      this.src =
        "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==";
    });
  return this;
};
