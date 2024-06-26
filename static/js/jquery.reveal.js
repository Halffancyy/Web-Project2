﻿(function (e) {
  "use strict";
  var t = !1;
  e(document).on("click", "a[data-reveal-id]", function (t) {
    t.preventDefault();
    var n = e(this).attr("data-reveal-id");
    e("#" + n).reveal(e(this).data());
  }),
    (e.fn.reveal = function (n) {
      var r = e(document),
        i = {
          animation: "fadeAndPop",
          animationSpeed: 300,
          closeOnBackgroundClick: !0,
          dismissModalClass: "close-reveal-modal",
          open: e.noop,
          opened: e.noop,
          close: e.noop,
          closed: e.noop,
        };
      return (
        (n = e.extend({}, i, n)),
        this.not(".reveal-modal.open").each(function () {
          function c() {
            u = !1;
          }
          function h() {
            u = !0;
          }
          function p() {
            var n = e(".reveal-modal.open");
            n.length === 1 && ((t = !0), n.trigger("reveal:close"));
          }
          function d() {
            u ||
              (h(),
              p(),
              i.addClass("open"),
              n.animation === "fadeAndPop" &&
                ((f.open.top = r.scrollTop() - o),
                (f.open.opacity = 0),
                i.css(f.open),
                a.fadeIn(n.animationSpeed / 2),
                i
                  .delay(n.animationSpeed / 2)
                  .animate(
                    { top: r.scrollTop() + s + "px", opacity: 1 },
                    n.animationSpeed,
                    function () {
                      i.trigger("reveal:opened");
                    }
                  )),
              n.animation === "fade" &&
                ((f.open.top = r.scrollTop() + s),
                (f.open.opacity = 0),
                i.css(f.open),
                a.fadeIn(n.animationSpeed / 2),
                i
                  .delay(n.animationSpeed / 2)
                  .animate({ opacity: 1 }, n.animationSpeed, function () {
                    i.trigger("reveal:opened");
                  })),
              n.animation === "none" &&
                ((f.open.top = r.scrollTop() + s),
                (f.open.opacity = 1),
                i.css(f.open),
                a.css({ display: "block" }),
                i.trigger("reveal:opened")));
          }
          function m() {
            u ||
              (h(),
              i.removeClass("open"),
              n.animation === "fadeAndPop" &&
                (i.animate(
                  { top: r.scrollTop() - o + "px", opacity: 0 },
                  n.animationSpeed / 2,
                  function () {
                    i.css(f.close);
                  }
                ),
                t
                  ? i.trigger("reveal:closed")
                  : a
                      .delay(n.animationSpeed)
                      .fadeOut(n.animationSpeed, function () {
                        i.trigger("reveal:closed");
                      })),
              n.animation === "fade" &&
                (i.animate({ opacity: 0 }, n.animationSpeed, function () {
                  i.css(f.close);
                }),
                t
                  ? i.trigger("reveal:closed")
                  : a
                      .delay(n.animationSpeed)
                      .fadeOut(n.animationSpeed, function () {
                        i.trigger("reveal:closed");
                      })),
              n.animation === "none" &&
                (i.css(f.close),
                t || a.css({ display: "none" }),
                i.trigger("reveal:closed")),
              (t = !1));
          }
          function g() {
            i.unbind(".reveal"),
              a.unbind(".reveal"),
              l.unbind(".reveal"),
              e("body").unbind(".reveal");
          }
          var i = e(this),
            s = parseInt(i.css("top"), 10),
            o = i.height() + s,
            u = !1,
            a = e(".reveal-modal-bg"),
            f = {
              open: {
                top: 0,
                opacity: 0,
                visibility: "visible",
                display: "block",
              },
              close: {
                top: s,
                opacity: 1,
                visibility: "hidden",
                display: "none",
              },
            },
            l;
          a.length === 0 &&
            ((a = e("<div />", { class: "reveal-modal-bg" }).insertAfter(i)),
            a.fadeTo("fast", 0.8)),
            i.bind("reveal:open.reveal", d),
            i.bind("reveal:close.reveal", m),
            i.bind("reveal:opened.reveal reveal:closed.reveal", c),
            i.bind("reveal:closed.reveal", g),
            i.bind("reveal:open.reveal", n.open),
            i.bind("reveal:opened.reveal", n.opened),
            i.bind("reveal:close.reveal", n.close),
            i.bind("reveal:closed.reveal", n.closed),
            i.trigger("reveal:open"),
            (l = e("." + n.dismissModalClass).bind("click.reveal", function () {
              i.trigger("reveal:close");
            })),
            n.closeOnBackgroundClick &&
              (a.css({ cursor: "pointer" }),
              a.bind("click.reveal", function () {
                i.trigger("reveal:close");
              })),
            e("body").bind("keyup.reveal", function (e) {
              e.which === 27 && i.trigger("reveal:close");
            });
        })
      );
    });
})(jQuery);
