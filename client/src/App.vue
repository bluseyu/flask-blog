<template>
    <router-view></router-view>
</template>

<script setup>

</script>

<style lang="scss" scoped>
// ================== _variable ==================
/* IMG URL */
$IMGURL: "../assets/img/" !default;

// Font size
$font-size: 1rem;
$font-size-xs: 0.8rem;
$font-size-sm: 1.2rem;
$font-size-md: 1.6rem;
$font-size-lg: 2.4rem;

// ================== _mixin ==================
/* 定义屏幕大小 */
$breakpoints: (
    "mb": "only screen and (max-width: 576px)",
    "xs": "only screen and (min-width: 480px)",
    "sm": "only screen and (min-width: 768px)",
    "md": "only screen and (min-width: 992px)",
    "lg": "only screen and (min-width: 1200px)",
    "pc": "only screen and (min-width: 1440px)",
    "pc-m": "only screen and (min-width: 1650px)",
    "pc-l": "only screen and (min-width: 1920px)",
    ) !default;

/* 媒体查询 */
@mixin respond-to($breakpoint) {
    $query: map-get($breakpoints, $breakpoint
);

// 如果超出设定范围则提示错误
@if not $query {
    @error "No value found for '#{$breakpoint}'. Please make sure it is defined in '$breakpoints' map.";
}

// 断点，校验$query的合法性
@media #{if(type-of($query) == 'string', unquote($query), inspect($query))} {
    @content;
}
}

/* 添加浏览器前缀 */
@mixin css3($property, $value) {

    @each $prefix in -webkit-,
    -moz-,
    -o-,
    "" {
        #{$prefix}#{$property}: $value;
    }
}

/* 文字强制换行 */
%word-break {
    word-wrap: break-word;
    word-break: break-all;
    white-space: pre-wrap;
}

/* 单行文字截断 */
%text-truncate {
    word-wrap: normal;
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
}

/* 多行文字截断 */
@mixin line-truncate($linenum: null) {
    display: -webkit-box;
    -webkit-line-clamp: $linenum;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* 文字隐藏 */
%text-hide {
    text-indent: -999rem;
}

/* 字母大写 */
%text-capital {
    text-transform: uppercase;
}

/* clear float 清除浮动 */
%clear {

    &:before,
    &:after {
        content: "";
        display: table;
    }

    &:after {
        clear: both;
    }
}

/* 弹性盒属性 */
%flexbox {
    @include css3(display, flex);
    @include css3(flex-flow, row);
    @include css3(flex-wrap, wrap);
    @include css3(box-pack, justify);
}

%hide {
    visibility: hidden;
    opacity: 0;
}

%show {
    visibility: visible;
    opacity: 1;
}

/* animation basic settings 动画基本设置 */
%animationBase {
    -webkit-animation-fill-mode: both;
    animation-fill-mode: both;
    -webkit-animation-fill-mode: forwards;
    animation-fill-mode: forwards;
}

/* transition 设置运动变形方式及时长 */
@mixin transition($content: null) {
    @include css3(transition, $content);
}

/* animation 设置动画方式及时长 */
@mixin animation($content: null) {
    @include css3(animation, $content);
}

// ================== _color ==================
/**
* light: 光明 !default
* dark：暗黑
* dusk: 薄暮
* volcano: 火山
* aurora: 极光
* geek: 极客
*/
$themes: (
    light: (),
    dark: (),
);

// ================== _handle ==================

//遍历主题map
@mixin themeify {

    @each $theme-name,
    $theme-map in $themes {
        $theme-map: $theme-map  !global;

        [data-theme="#{$theme-name}"] & {
            @content;
        }
    }
}

//根据Key获取颜色的function
@function themed($key) {
    @return map-get($theme-map, $key);
}

//获取背景颜色
@mixin background-color($color) {
    @include themeify {
        background-color: themed($color) !important;
    }
}

//获取字体颜色
@mixin font-color($color) {
    @include themeify {
        color: themed($color) !important;
    }
}

//获取边框颜色
@mixin border-color($color) {
    @include themeify {
        border-color: themed($color) !important;
    }
}

//获取边框渐变色
@mixin border-linear($width, $from, $to, $radius) {
    @include themeify {
        border: $width solid transparent;
        border-image: linear-gradient(45deg, themed($from), themed($to)) 1;
        clip-path: inset(0 round $radius);
    }
}

//获取阴影颜色
@mixin box-shadow($hx, $vy, $spread, $color) {
    @include themeify {
        box-shadow: $hx $vy $spread themed($color) !important;
    }
}

//获取背景色渐变
@mixin linear-gradient($deg, $from, $to) {
    @include themeify {
        background-image: linear-gradient($deg, themed($from), themed($to));
    }
}

//获取文字颜色渐变
@mixin font-gradient($from, $to) {
    @include themeify {
        background-image: linear-gradient(to bottom, themed($from), themed($to));
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
    }
}

// 获取背景图片
@mixin background-image($imgurl) {
    @include themeify {
        background-image: themed($imgurl);
    }
}

// ================== animate ==================

// ================== common ==================

// ================== theme ==================
</style>
