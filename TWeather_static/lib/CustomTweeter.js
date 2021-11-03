(function($, block) {
block.fn.tweetsmodern = function(config) {
    var options = $.extend({
        memory: 20
    }, config);

    // create the necessary HTML in the block container
    this.$element.append('<ol class="tweet-list stream-items"></ol>');

    // store list for later
    var $list = this.$element.find('ol');


    // register default handler for handling tweet data
    this.actions(function(e, tweet){
        var html = tweet['html'].slice(0, (-71) % tweet['html'].length)
        var $container = $("<div></div>");
        $container.prepend($(html));
        $container.prepend($("<script src=lib/widget.js></script>"))
        $list.prepend($container);
    });

    return this.$element;
};
})(jQuery, block);