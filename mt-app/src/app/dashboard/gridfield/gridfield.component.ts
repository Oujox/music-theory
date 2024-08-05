import { Component } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import {
  GridsterModule,
  GridsterConfig,
  GridsterItem,
} from 'angular-gridster2';

@Component({
  selector: 'app-gridfield',
  standalone: true,
  imports: [GridsterModule, MatIconModule],
  templateUrl: './gridfield.component.html',
  styleUrl: './gridfield.component.scss',
})
export class GridfieldComponent {
  options: GridsterConfig = {};
  dashboard: Array<GridsterItem> = [];

  innerWidth = window.innerWidth;

  ngOnInit(): void {
    this.options = {
      gridType: 'scrollVertical', // 固定縦横比を縦スクロールで対応
      // gridType: 'scrollHorizontal', // 固定縦横比を水平スクロールで対応
      draggable: {
        // ドラッグ設定
        enabled: true, // ドラッグ許可
        ignoreContent: true, // dragHandleClassのみドラッグイベントを可能にする
        dragHandleClass: 'draggable-handler', // ここで指定したクラスのみドラッグイベントを可能にする
      },
      resizable: {
        // リサイズ設定
        enabled: true, // リサイズを許可する
      },
      swap: true, // 入れ替えを許可する
      displayGrid: 'always', // グリッド線を常に表示
      minCols: 7, // 最小列数
      maxCols: 7, // 最大列数(minCols以上はドラッグで表示される)
      minRows: 7, // 最小行数
      maxRows: 7, // 最大行数(minRows以上はドラッグで表示される)
      maxItemCols: 5, // アイテムの最大列数
      maxItemRows: 5, // アイテムの最大行数
      compactType: 'none', // 整列しない(自由)
      pushItems: true, // リサイズとドラッグでアイテムを押しのける
      mobileBreakpoint: 640, // 画面の幅が640px以下でグリッドを解除しアイテムを1列にする
    };

    this.dashboard = [
      { cols: 3, rows: 4, y: 1, x: 2 }, // 初期値 横3マス, 縦4マス,をy1, x2の位置に配置
    ];
  }

  removeItem(index: number): void {
    this.dashboard.splice(index, 1); // index番目を1つ取り除く
  }

  addItem(): void {
    this.dashboard.push({ cols: 3, rows: 3, y: 0, x: 0 });
  }
}
